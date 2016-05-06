gst-launch-0.10 -v audiotestsrc ! audioconvert ! lame bitrate=16 ! udpsink port=3000 host=127.0.0.1
