# -*- coding: utf-8 -*-
"""Maverick

Author: AlanDecode | 熊猫小A
Link:   https://www.imalan.cn
GitHub: https://github.com/AlanDecode
"""

import os

if not os.path.exists('./config.py'):
    raise BaseException('No config.py! Exiting...')


import config
from Maverick.Builder import Builder
from Maverick.Utils import print_color, Color


def main():
    conf = config.g_conf

    print_color('Site prefix: ' + conf.site_prefix, Color.GREEN.value)
    print_color('Source dir: ' + conf.source_dir, Color.GREEN.value)
    print_color('Build dir: ' + conf.build_dir, Color.GREEN.value)

    builder = Builder(conf)
    builder.build_all()


if __name__ == "__main__":
    main()
