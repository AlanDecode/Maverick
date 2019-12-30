# -*- coding: utf-8 -*-
"""Configuration
"""

import os
import sys


class Config(object):
    def update_fromfile(self, filepath=None):
        if filepath is None:
            return

        sys.path.append(os.path.dirname(filepath))

        name, _ = os.path.splitext(os.path.basename(filepath))
        module = __import__(name)

        attrs = dir(module)
        for attr in attrs:
            if attr.startswith('__'):
                continue
            setattr(self, attr, getattr(module, attr))

    def update_fromenv(self):
        attrs = dir(self)
        for attr in attrs:
            if attr.startswith('__'):
                continue
            setattr(self, attr, os.getenv(attr, getattr(self, attr)))

    # For Maverick
    site_prefix = "/"
    source_dir = "./test_src/"
    build_dir = "./test_dist/"

    # to use theme in another local folder, set:
    # template = {
    #     "name": "<name of template>",
    #     "type": "local",
    #     "path": "<path to template>"
    # }
    template = "Galileo"
    index_page_size = 10
    archives_page_size = 30
    fetch_remote_imgs = False
    enable_jsdelivr = {
        "enabled": False,
        "repo": ""
    }
    locale = "Asia/Shanghai"
    category_by_folder = False

    # For site
    site_name = ""
    site_logo = ""
    site_build_date = ""
    author = ""
    email = ""
    author_homepage = ""
    description = ""
    key_words = []
    language = "english"
    background_img = ""
    external_links = []
    nav = []

    social_links = []

    valine = {
        "enable": False,
        "appId": "",
        "appKey": "",
        "notify": "false",
        "visitor": "false",
        "recordIP": "false",
        "serverURLs": None,
        "placeholder": "Just go go~"
    }

    head_addon = ""

    footer_addon = ""

    body_addon = ""


g_conf = Config()
