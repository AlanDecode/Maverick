# -*- coding: utf-8 -*-
"""Configuration
"""

import os


class Config(object):
    # For Maverick
    site_prefix = "/"
    source_dir = "./test_src/"
    build_dir = "./test_dist/"
    template = "Galileo"
    index_page_size = 10
    archives_page_size = 30
    fetch_remote_imgs = False
    locale = "Asia/Shanghai"

    # For site
    site_name = "Maverick"
    site_logo = "${site_prefix}android-chrome-512x512.png"
    site_build_date = "2019-12-06T12:00+08:00"
    author = "AlanDecode"
    email = "hi@imalan.cn"
    author_homepage = "https://www.imalan.cn"
    description = "This is Maverick, a static blog generator built with Python. Theme Galileo."
    key_words = ["Maverick", "AlanDecode", "Galileo", "blog"]
    language = 'zh-CN'
    external_links = [
        {
            "name": "AlanDecode/Maverick",
            "url": "https://github.com/AlanDecode/Maverick",
            "brief": "🏄‍ Go My Own Way."
        },
        {
            "name": "Triple NULL",
            "url": "https://www.imalan.cn",
            "brief": "Home page for AlanDecode."
        }
    ]
    nav = [
        {
            "name": "Home",
            "url": "${site_prefix}",
            "target": "_self"
        },
        {
            "name": "Archives",
            "url": "${site_prefix}archives/",
            "target": "_self"
        },
        {
            "name": "About",
            "url": "${site_prefix}about/",
            "target": "_self"
        }
    ]

    social_links = [
        {
            "name": "Twitter",
            "url": "https://twitter.com/AlanDecode",
            "icon": "gi gi-twitter"
        },
        {
            "name": "GitHub",
            "url": "https://github.com/AlanDecode",
            "icon": "gi gi-github"
        },
        {
            "name": "Weibo",
            "url": "https://weibo.com/5245109677/",
            "icon": "gi gi-weibo"
        }
    ]

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

    head_addon = r"""
<!-- Content here will be added before </head>. -->
"""

    footer_addon = r"""
<!-- Content here will be added to <footer> tag.-->
"""

    body_addon = r"""
<!-- Content here will be added before </body>. -->
"""

g_conf = Config()

# Update config from env
g_conf.site_prefix = os.getenv("site_prefix", g_conf.site_prefix)
g_conf.source_dir = os.getenv("source_dir", g_conf.source_dir)
g_conf.build_dir = os.getenv("build_dir", g_conf.build_dir)
g_conf.template = os.getenv("template", g_conf.template)
g_conf.index_page_size = int(os.getenv("index_page_size", g_conf.index_page_size))
g_conf.archives_page_size = int(os.getenv("archives_page_size", g_conf.archives_page_size))
