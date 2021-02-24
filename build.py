#!/usr/bin/env python
"""Maverick

Author: AlanDecode | 熊猫小A
Link:   https://www.imalan.cn
GitHub: https://github.com/AlanDecode
"""

from Maverick.Utils import print_color, Color
from Maverick.Builder import Builder
from Maverick.Config import g_conf
import os
import sys
import getopt


def main(argv):
    try:
        opts, _ = getopt.getopt(argv, "c:", "config=")
    except getopt.GetoptError:
        pass

    opts = dict(opts)

    if '-c' in opts or '--config' in opts:
        g_conf.update_fromfile(opts.get('-c', None))
        g_conf.update_fromfile(opts.get('--config', None))
    else:
        if os.path.exists('./config.py'):
            g_conf.update_fromfile('./config.py')

    g_conf.update_fromenv()

    print_color('Site prefix: ' + g_conf.site_prefix, Color.GREEN.value)
    print_color('Source dir: ' + g_conf.source_dir, Color.GREEN.value)
    print_color('Build dir: ' + g_conf.build_dir, Color.GREEN.value)

    builder = Builder(g_conf)
    builder.build_all()


if __name__ == "__main__":
    main(sys.argv[1:])
