# fun_random_videos
The [WebViewScreenSaver](https://github.com/liquidx/webviewscreensaver) is a screen saver for MacOS that allows you to put websites, or even videos, as your screen saver. I find it fun to have fun youtube videos as screen savers but since I like a bunch of those I thought it would be nice to have a way to set a list of those and make the WebViewScreenSaver show one of the videos for each time the OS loads a screen saver. The code in this repo does just that.

# How to run this?

Requires python 3.

```bash
python  fun_random_videos.py
```
# I have a bunch of funny videos, how can I add them?

Just edit the `fun_videos.ini` file adding and/or removing the example video links and restart the server. Remember to add the `embed` links, not the regular `watch` ones. Here is how the video list session of the ini file should look like:

```ini
[fun_videos]
videos=
# jonny castaway
  https://www.youtube.com/embed/NTg5fXyujnM
# gandalf amazing sax guy
  https://www.youtube.com/embed/G1IbRujko-A
# keyboard cat
  https://www.youtube.com/embed/O2ulyJuvU3Q
```

# How to configure the WebViewScreenSaver?

First, follow the instructions in [here](https://github.com/liquidx/webviewscreensaver#usage) to install it. After that, add the address to reach the `fun_random_videos` server into the webview screen saver configs and that is it. It should look something like this:

![alt text](https://github.com/moisesber/fun_random_videos/blob/master/screenshots/config-screenshot.png "Config example")

Screenshot of everything working:

![alt text](https://github.com/moisesber/fun_random_videos/blob/master/screenshots/screensaver.screenshot.png "Screensaver example")
