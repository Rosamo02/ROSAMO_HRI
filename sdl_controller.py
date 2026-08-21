import sdl2
import sdl2.ext
import threading
import time


class SDLController:
    def __init__(self, mainwindow):
        self.main = mainwindow
        self.rb_down = False

        print("\n[SDL2] Initializing controller system...")
        sdl2.SDL_Init(sdl2.SDL_INIT_GAMECONTROLLER)

        num_joy = sdl2.SDL_NumJoysticks()
        print(f"[SDL2] Joysticks detected: {num_joy}")

        self.controller = None
        for i in range(num_joy):
            if sdl2.SDL_IsGameController(i):
                self.controller = sdl2.SDL_GameControllerOpen(i)
                print("[SDL2] Controller connected:",
                      sdl2.SDL_GameControllerName(self.controller))
                break

        if self.controller is None:
            print("No controller detected")

        # 20 Hz publish rate
        self.publish_rate = 20.0
        self.publish_period = 1.0 / self.publish_rate

        self.thread = threading.Thread(target=self.poll, daemon=True)
        self.thread.start()

    def poll(self):
        event = sdl2.SDL_Event()
        next_publish_time = time.monotonic()

        while True:
            # Process all pending SDL events
            while sdl2.SDL_PollEvent(event):
                if event.type == sdl2.SDL_CONTROLLERAXISMOTION:
                    self.handle_axis(event.caxis)

                elif event.type == sdl2.SDL_CONTROLLERBUTTONDOWN:
                    self.handle_button(event.cbutton, True)

                elif event.type == sdl2.SDL_CONTROLLERBUTTONUP:
                    self.handle_button(event.cbutton, False)

            # Publish at fixed 20 Hz
            now = time.monotonic()
            if now >= next_publish_time:
                self.publish_current_cmd()
                next_publish_time += self.publish_period

                # Prevent drift if loop falls behind badly
                if now > next_publish_time + self.publish_period:
                    next_publish_time = now + self.publish_period

            sdl2.SDL_Delay(1)

    def handle_axis(self, axis_event):
        if self.main.current_mode != "controller":
            return

        teleop = self.main.teleop_controller
        value = axis_event.value / 32767.0

        # Deadzone
        if abs(value) < 0.03:
            value = 0.0

        scaled_value = value

        if axis_event.axis == sdl2.SDL_CONTROLLER_AXIS_LEFTX:
            teleop.angular = -scaled_value

        elif axis_event.axis == sdl2.SDL_CONTROLLER_AXIS_LEFTY:
            teleop.linear = -scaled_value

        elif axis_event.axis == sdl2.SDL_CONTROLLER_AXIS_TRIGGERLEFT:
            trigger_value = max(0.0, axis_event.value / 32767.0)

            if trigger_value > 0.1 and self.rb_down:
                teleop.tool = -1.0
            else:
                teleop.tool = 0.0

    def handle_button(self, button_event, pressed):
        if self.main.current_mode != "controller":
            return

        teleop = self.main.teleop_controller

        # RB dead-man switch
        if button_event.button == sdl2.SDL_CONTROLLER_BUTTON_RIGHTSHOULDER:
            print("[RB] pressed:", pressed)
            self.rb_down = pressed

            if not pressed:
                teleop.linear = 0.0
                teleop.angular = 0.0
                teleop.tool = 0.0
                teleop.send_cmd()

        elif button_event.button == sdl2.SDL_CONTROLLER_BUTTON_LEFTSHOULDER:
            print("[LB] pressed:", pressed)

            if pressed and self.rb_down:
                teleop.tool = 1.0
            else:
                teleop.tool = 0.0


    def publish_current_cmd(self):
        if self.main.current_mode != "controller":
            return

        teleop = self.main.teleop_controller

        if self.rb_down:
            teleop.send_cmd()
        else:
            #If the deadman trigger is off, it sends empty commands
            teleop.linear = 0.0
            teleop.angular = 0.0
            teleop.tool = 0.0
            teleop.send_cmd()
