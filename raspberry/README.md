#### Video streaming with *gstreamer*

* First install gstreamer both Raspberry Pi and ground station:

```
$ sudo apt-get install gstreamer1.0-tools
```

* Than use these command to stream video

On Raspberry Pi:
```
$ raspivid -fps 30 -h 1080 -w 1920 -vf -n -t 0 -b 200000 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96! gdppay ! tcpserversink host=192.168.x.x port=xxxx
```

On Ground Station (Linux):
```
$ gst-launch-0.10 -v tcpclientsrc host=192.168.x.x port=xxxx ! gdpdepay ! rtph264depay ! ffdec_h264 ! ffmpegcolorspace ! autovideosink sync=false
```
