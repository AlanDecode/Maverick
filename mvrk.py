#!/usr/bin/env python3
"""Maverick

Author: AlanDecode | 熊猫小A
Link:   https://www.imalan.cn
GitHub: https://github.com/AlanDecode
"""

import argparse

from Maverick.Utils import print_color, Color
from Maverick.Builder import Builder
from Maverick.Config import g_conf


def _get_parser() -> argparse.ArgumentParser:
  _parser = argparse.ArgumentParser()
  _parser.add_argument('--config', '-c', required=True, help='Config file path')
  _parser.add_argument('--source_dir', '-s', default='', help='Source dir')
  _parser.add_argument('--build_dir', '-b', default='', help='Build dir')
  return _parser


def main():
  args = _get_parser().parse_args()

  g_conf.update_fromfile(args.config)
  g_conf.update_fromenv()
  if args.source_dir:
    g_conf.source_dir = args.source_dir
  if args.build_dir:
    g_conf.build_dir = args.build_dir

  print_color('Site prefix: ' + g_conf.site_prefix, Color.GREEN.value)
  print_color('Source dir: ' + g_conf.source_dir, Color.GREEN.value)
  print_color('Build dir: ' + g_conf.build_dir, Color.GREEN.value)

  builder = Builder(g_conf)
  builder.build_all()


if __name__ == "__main__":
  main()
