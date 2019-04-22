import random
import json
import configparser
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

default_fun_videos = [
    "https://www.youtube.com/embed/NTg5fXyujnM",  # jonny castaway
    "https://www.youtube.com/embed/G1IbRujko-A",  # gandalf amazing sax guy
    "https://www.youtube.com/embed/O2ulyJuvU3Q",  # keyboard cat
]
config = configparser.ConfigParser()
config.read("fun_videos.ini")
config_videos_list = None

if "fun_videos" in config.sections():
    if "videos" in config["fun_videos"]:
        config_videos_list_str = config.get("fun_videos", "videos")
        config_videos_list = re.split(",|\n| ", config_videos_list_str)

        # cleaning up formatting ini file formatting issues
        if "" in config_videos_list:
            config_videos_list.remove("")

width = "1440"
height = "900"

if "display_settings" in config.sections():
    if "width" in config["display_settings"]:
        width = config.get("display_settings", "width")

    if "height" in config["display_settings"]:
        height = config.get("display_settings", "height")

port = 8000
if "server" in config.sections():
    if "port" in config["server"]:
        port = config.get("server", "port")

if not config_videos_list:
    config_videos_list = default_fun_videos

random.shuffle(config_videos_list)
shuffled_videos = config_videos_list


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    video_index = 0

    @staticmethod
    def increment_video_index():
        SimpleHTTPRequestHandler.video_index += 1

        if SimpleHTTPRequestHandler.video_index >= len(shuffled_videos):
            SimpleHTTPRequestHandler.video_index = 0

    def get_video_string(self):
        # triggers autoplay and full screen mode
        video_sufix = "?rel=0&autoplay=1"

        video = shuffled_videos[SimpleHTTPRequestHandler.video_index]

        SimpleHTTPRequestHandler.increment_video_index()
        return "%s%s" % (video, video_sufix)

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(
            bytes(
                """<!DOCTYPE html><html><body><iframe width="%s" height="%s" src="%s"></iframe></body></html>"""
                % (width, height, self.get_video_string()),
                "UTF-8",
            )
        )


httpd = HTTPServer(("localhost", 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
