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
        'rtpjitterbuffer latency=250 drop-on-latency=true do-lost=true ! '
        'rtph264depay ! h264parse ! avdec_h264 ! '
        'videoconvert ! video/x-raw,format=RGB ! '
        'appsink name=appsink emit-signals=true max-buffers=1 drop=true sync=false'
    )

    pipeline_cam0_lq = (
        'udpsrc address=:: port=5002 buffer-size=4194304 '
        'caps="application/x-rtp,media=video,encoding-name=H264,payload=96,clock-rate=90000" ! '
        'rtpjitterbuffer latency=200 drop-on-latency=true do-lost=true ! '
        'rtph264depay ! h264parse ! avdec_h264 ! '
        'videoconvert ! video/x-raw,format=RGB ! '
        'appsink name=appsink emit-signals=true max-buffers=1 drop=true sync=false'
    )

    pipeline_cam1 = (
        'udpsrc address=:: port=5001 buffer-size=4194304 '
        'caps="application/x-rtp,media=video,encoding-name=H264,payload=96,clock-rate=90000" ! '
        'rtpjitterbuffer latency=250 drop-on-latency=true do-lost=true ! '
        'rtph264depay ! h264parse ! avdec_h264 ! '
        'videoconvert ! video/x-raw,format=RGB ! '
        'appsink name=appsink emit-signals=true max-buffers=1 drop=true sync=false'
    )

    pipeline_cam1_lq = (
        'udpsrc address=:: port=5003 buffer-size=4194304 '
        'caps="application/x-rtp,media=video,encoding-name=H264,payload=96,clock-rate=90000" ! '
        'rtpjitterbuffer latency=200 drop-on-latency=true do-lost=true ! '
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
        (158, 392), (188, 364), (218, 338), (248, 318),
        (278, 302), (308, 294), (338, 290), (368, 292),
        (398, 300), (428, 313), (458, 331), (488, 354),
        (518, 379), (548, 408),
    ])

    window.primary_camera_widget_lq.set_toolpath_pixels([
        (132, 327), (157, 303), (182, 282), (207, 265),
        (232, 252), (257, 245), (282, 242), (307, 243),
        (332, 250), (357, 261), (382, 276), (407, 295),
        (432, 316), (457, 340),
    ])

    window.secondary_camera_widget.set_toolpath_pixels([
        (360, 204), (358, 233), (351, 261), (341, 287),
        (326, 310), (309, 329), (289, 343), (268, 351),
        (245, 354), (223, 351), (201, 343), (182, 329),
        (164, 310), (150, 287), (139, 261), (133, 233),
        (131, 204), (133, 175), (139, 147), (150, 120),
        (164, 98), (182, 79), (201, 65), (223, 57),
        (245, 54), (268, 57), (289, 65), (309, 79),
        (326, 98), (341, 120), (351, 147), (358, 175),
        (360, 204),
    ])

    window.secondary_camera_widget_lq.set_toolpath_pixels([
        (360, 204), (358, 233), (351, 261), (341, 287),
        (326, 310), (309, 329), (289, 343), (268, 351),
        (245, 354), (223, 351), (201, 343), (182, 329),
        (164, 310), (150, 287), (139, 261), (133, 233),
        (131, 204), (133, 175), (139, 147), (150, 120),
        (164, 98), (182, 79), (201, 65), (223, 57),
        (245, 54), (268, 57), (289, 65), (309, 79),
        (326, 98), (341, 120), (351, 147), (358, 175),
        (360, 204),
    ])

    window.ui.videoLayout.addWidget(window.primary_camera_widget)
    window.ui.videoLayout_lq.addWidget(window.primary_camera_widget_lq)
    window.ui.secondaryVideoLayout.addWidget(window.secondary_camera_widget)
    window.ui.secondaryVideoLayout_lq.addWidget(window.secondary_camera_widget_lq)

    print("after GstVideoWidget")
