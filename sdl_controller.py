# sdl_controller.py
import sdl2
import sdl2.ext
import threading
from PySide6.QtCore import QTimer

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

        # Start polling thread
        self.thread = threading.Thread(target=self.poll, daemon=True)
        self.thread.start()

    def poll(self):
        event = sdl2.SDL_Event()

        while True:
            while sdl2.SDL_PollEvent(event):
                if event.type == sdl2.SDL_CONTROLLERAXISMOTION:
                    self.handle_axis(event.caxis)

                elif event.type == sdl2.SDL_CONTROLLERBUTTONDOWN:
                    self.handle_button(event.cbutton, True)

                elif event.type == sdl2.SDL_CONTROLLERBUTTONUP:
                    self.handle_button(event.cbutton, False)

            sdl2.SDL_Delay(5)

    def handle_axis(self, axis_event):
        if self.main.current_mode != "controller":
            return

        value = axis_event.value / 32767.0

        # Dead-man switch not pressed-> stop
        if not self.rb_down:
            self.main.linear = 0.0
            self.main.angular = 0.0
            self.main.update_cmd()
            return

        if axis_event.axis == sdl2.SDL_CONTROLLER_AXIS_LEFTX:
            self.main.angular = -value
        elif axis_event.axis == sdl2.SDL_CONTROLLER_AXIS_LEFTY:
            self.main.linear = -value

        print(f"[CONTROLLER] linear={self.main.linear:.2f}, angular={self.main.angular:.2f}")

        # Auto-repeat
        for _ in range(20):
            self.main.update_cmd()
            sdl2.SDL_Delay(1)

    def handle_button(self, button_event, pressed):
        if self.main.current_mode != "controller":
            return

        # RB dead-man switch
        if button_event.button == sdl2.SDL_CONTROLLER_BUTTON_RIGHTSHOULDER:
            print("[RB] pressed:", pressed)
            self.rb_down = pressed

            if not pressed:
                self.main.linear = 0.0
                self.main.angular = 0.0
                self.main.update_cmd()
