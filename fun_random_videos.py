import random
import json
import configparser
import re
import argparse
import sys
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
c_format = logging.Formatter('%(asctime)s-%(process)d-%(levelname)s: %(message)s')
c_handler.setFormatter(c_format)
c_handler.setLevel(logging.DEBUG)
logger.addHandler(c_handler)


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--config-path', help='Full path to the configuration file.',
                   default='fun_videos.ini')

args = parser.parse_args()
config_path = args.config_path

default_fun_videos = [
    "https://www.youtube.com/embed/NTg5fXyujnM",  # jonny castaway
    "https://www.youtube.com/embed/G1IbRujko-A",  # gandalf amazing sax guy
    "https://www.youtube.com/embed/O2ulyJuvU3Q",  # keyboard cat
]
config = configparser.ConfigParser()
logger.warning('Reading configs from file %s', config_path)
config.read(config_path)
config_videos_list = None

if "fun_videos" in config.sections():
    logger.warning('Found fun_videos defined in config file.')
    if "videos" in config["fun_videos"]:
        config_videos_list_str = config.get("fun_videos", "videos")
        config_videos_list = re.split(",|\n| ", config_videos_list_str)
        logger.warning('Videos found were: %s', config_videos_list)

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
logger.warning('Display settings found were: W: %s and H: %s', width, height )

port = 8000
if "server" in config.sections():
    if "port" in config["server"]:
        port = config.get("server", "port")

if not config_videos_list:
    config_videos_list = default_fun_videos

random.shuffle(config_videos_list)
shuffled_videos = config_videos_list

logger.warning('Running HTTP server on port %s', port)

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
                """<!DOCTYPE html>
                    <html>
                        <body>
                            <p id="funvideo"></p>
                            <script>
                                var w = window.innerWidth;
                                var h = window.innerHeight;
                                document.getElementById("funvideo").innerHTML = '<iframe width="' + w + '" height="'+ h +'" src="%s"</iframe>';
                            </script>
                        </body>
                    </html>"""
                % (self.get_video_string()),
                "UTF-8",
            )
        )

httpd = HTTPServer(("localhost", 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
