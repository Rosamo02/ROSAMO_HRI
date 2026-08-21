# gstreamer_setup.py
#Improtant to remember, the whole reason that I placed this in a different file was because this launches simultaneously with the rest of the __init__ was causing something to break
#I changed it to a separate file to avoid that, but in practice, this is simply a continuation of the __init__ on mainwindow.py
def setup_gstreamer_window(window):
    import gi
    gi.require_version("Gst", "1.0")
    from gi.repository import Gst

    from gst_video_widget import GstVideoWidget

    print("before Gst.init")
    Gst.init(None)
    print("after Gst.init")

    pipeline_cam0 = (
        'udpsrc address=:: port=5000 buffer-size=4194304 '
        'caps="application/x-rtp,media=video,encoding-name=H264,payload=96,clock-rate=90000" ! '
        'rtpjitterbuffer latency=50 drop-on-latency=true do-lost=true ! '
        'rtph264depay ! h264parse ! avdec_h264 ! '
        'videoconvert ! video/x-raw,format=RGB ! '
        'appsink name=appsink emit-signals=true max-buffers=1 drop=true sync=false'
    )

    pipeline_cam0_lq = (
        'udpsrc address=:: port=5002 buffer-size=4194304 '
        'caps="application/x-rtp,media=video,encoding-name=H264,payload=96,clock-rate=90000" ! '
        'rtpjitterbuffer latency=75 drop-on-latency=true do-lost=true ! '
        'rtph264depay ! h264parse ! avdec_h264 ! '
        'videoconvert ! video/x-raw,format=RGB ! '
        'appsink name=appsink emit-signals=true max-buffers=1 drop=true sync=false'
    )

    pipeline_cam1 = (
        'udpsrc address=:: port=5001 buffer-size=4194304 '
        'caps="application/x-rtp,media=video,encoding-name=H264,payload=96,clock-rate=90000" ! '
        'rtpjitterbuffer latency=50 drop-on-latency=true do-lost=true ! '
        'rtph264depay ! h264parse ! avdec_h264 ! '
        'videoconvert ! video/x-raw,format=RGB ! '
        'appsink name=appsink emit-signals=true max-buffers=1 drop=true sync=false'
    )

    pipeline_cam1_lq = (
        'udpsrc address=:: port=5003 buffer-size=4194304 '
        'caps="application/x-rtp,media=video,encoding-name=H264,payload=96,clock-rate=90000" ! '
        'rtpjitterbuffer latency=75 drop-on-latency=true do-lost=true ! '
        'rtph264depay ! h264parse ! avdec_h264 ! '
        'videoconvert ! video/x-raw,format=RGB ! '
        'appsink name=appsink emit-signals=true max-buffers=1 drop=true sync=false'
    )

    print("before GstVideoWidget")

    window.primary_camera_widget = GstVideoWidget(pipeline_cam0)
    window.primary_camera_widget_lq = GstVideoWidget(pipeline_cam0_lq)
    window.secondary_camera_widget = GstVideoWidget(pipeline_cam1)
    window.secondary_camera_widget_lq = GstVideoWidget(pipeline_cam1_lq)

    window.primary_camera_widget.set_toolpath_pixels([
        (148, 372),  # Extra point on the left
        (178, 354), (208, 337), (238, 322), (268, 310),
        (298, 301), (328, 296), (358, 293), (388, 295),
        (418, 300), (448, 308), (478, 320), (508, 335),
        (538, 352), (568, 370),
    ])

    window.primary_camera_widget_lq.set_toolpath_pixels([
        (123, 310),  # Extra point on the left
        (148, 295), (173, 281), (198, 268), (223, 258),
        (248, 251), (273, 247), (298, 244), (323, 246),
        (348, 250), (373, 257), (398, 267), (423, 279),
        (448, 293), (473, 308),
    ])

    window.secondary_camera_widget.set_toolpath_pixels([
        (360, 214), (358, 243), (351, 271), (341, 297),
        (326, 320), (309, 339), (289, 353), (268, 361),
        (245, 364), (223, 361), (201, 353), (182, 339),
        (164, 320), (150, 297), (139, 271), (133, 243),
        (131, 214), (133, 185), (139, 157), (150, 130),
        (164, 108), (182, 89), (201, 75), (223, 67),
        (245, 64), (268, 67), (289, 75), (309, 89),
        (326, 108), (341, 130), (351, 157), (358, 185),
        (360, 214),
    ])

    window.secondary_camera_widget_lq.set_toolpath_pixels([
        (360, 214), (358, 243), (351, 271), (341, 297),
        (326, 320), (309, 339), (289, 353), (268, 361),
        (245, 364), (223, 361), (201, 353), (182, 339),
        (164, 320), (150, 297), (139, 271), (133, 243),
        (131, 214), (133, 185), (139, 157), (150, 130),
        (164, 108), (182, 89), (201, 75), (223, 67),
        (245, 64), (268, 67), (289, 75), (309, 89),
        (326, 108), (341, 130), (351, 157), (358, 185),
        (360, 214),
    ])

    window.ui.videoLayout.addWidget(window.primary_camera_widget)
    window.ui.videoLayout_lq.addWidget(window.primary_camera_widget_lq)
    window.ui.secondaryVideoLayout.addWidget(window.secondary_camera_widget)
    window.ui.secondaryVideoLayout_lq.addWidget(window.secondary_camera_widget_lq)

    print("after GstVideoWidget")
