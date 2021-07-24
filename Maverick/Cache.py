# -*- coding: utf-8 -*-
"""Handle cache
"""

import os
import json
import shutil
import urllib.request as request
from urllib.parse import urlparse

from PIL import Image
from PIL import ImageFile

from .Config import g_conf
from .Router import Router
from .Utils import (unify_joinpath, print_color, Color, safe_read, safe_write,
                    gen_hash)

g_used_imgs = None
g_sizeinfo_cache = None


def quickQueryImgSize(src):
  """get size info by downloading small part of it
    """
  try:
    with request.urlopen(src) as file:
      p = ImageFile.Parser()
      while True:
        data = file.read(1024)
        if not data:
          break
        p.feed(data)
        if p.image:
          return list(p.image.size)
  except BaseException as e:
    print_color('fetch error: ' + src, Color.RED.value)
    print_color(e, Color.RED.value)
    return None


def cache_img(src, base_path):
  """Gen image cache

    1. find image in cache dir
    2. if src is remote URL, download it or call quickQueryImgSize
    3. treat src as absolute path and find it
    3. treat src as relative path and find it
    """
  global g_used_imgs
  global g_sizeinfo_cache

  json_path = unify_joinpath(g_conf._cache_dir, 'tmp', 'used_imgs.json')
  sizeinfo_json_path = unify_joinpath(g_conf._cache_dir, 'sizeinfo.json')
  cache_dir = g_conf._cache_dir

  if g_used_imgs is None:
    g_used_imgs = set(json.loads(safe_read(json_path) or '[]'))
  if g_sizeinfo_cache is None:
    g_sizeinfo_cache = json.loads(safe_read(sizeinfo_json_path) or '{}')

  def log_and_return(filename):
    global g_used_imgs
    global g_sizeinfo_cache

    g_used_imgs = g_used_imgs | set([filename])

    info = {"src": '', "width": -1, "height": -1}

    # if enable jsDelivr CDN, add prefix
    # if not, fallback (site_prefix) will be used
    router = Router(g_conf)
    static_prefix = router.gen_static_file_prefix()
    info['src'] = "%sarchives/assets/%s" % (static_prefix, filename)

    if filename in g_sizeinfo_cache:  # if size info in cache
      info['width'] = g_sizeinfo_cache[filename][0]
      info['height'] = g_sizeinfo_cache[filename][1]
      print_color(
          "Sizeinfo hit cache: %s (%s, %s)" %
          (src, info['width'], info['height']), Color.GREEN.value)
    else:
      try:
        img = Image.open(unify_joinpath(cache_dir, filename))
        info['width'] = img.size[0]
        info['height'] = img.size[1]
        print_color(
            "Parsed sizeinfo from local: %s (%s, %s)" %
            (src, info['width'], info['height']), Color.GREEN.value)
        g_sizeinfo_cache[filename] = [img.size[0], img.size[1]]
      except IOError:
        print_color("Pars sizeinfo from local failed", Color.RED.value)

    return info

  src_md5 = gen_hash(src)

  # find image in cache dir
  os.makedirs(cache_dir, exist_ok=True)
  cached_imgs = [name for name in os.listdir(cache_dir)]
  for name in cached_imgs:
    if name.split('.')[0].lower() == src_md5.lower():  # in cache dir
      # print_color("Image hit cache: " + src, Color.GREEN.value)
      return log_and_return(name)

  # if it is remote image
  if src.startswith('http'):
    if g_conf.fetch_remote_imgs:
      # download and treat it as local image
      try:
        suffix = urlparse(src).path.split('.')[-1]
        filename = '.'.join([src_md5, suffix])

        proxy = request.ProxyHandler({})
        opener = request.build_opener(proxy)
        opener.addheaders = [('User-Agent',
                              r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              r'AppleWebKit/537.36(KHTML, like Gecko) '
                              r'Chrome/78.0.3904.108 Safari/537.36')]
        request.install_opener(opener)

        print_color("Trying to download: " + src, Color.BLUE.value)
        request.urlretrieve(src, unify_joinpath(cache_dir, filename))

        return log_and_return(filename)
      except BaseException as e:
        print_color('Fetch error: ' + src, Color.RED.value)
        print_color(e, Color.RED.value)
        return {"src": src, "width": -1, "height": -1}
    else:
      # download small part of it
      info = {"src": src, "width": -1, "height": -1}

      if src in g_sizeinfo_cache:
        info['width'] = g_sizeinfo_cache[src][0]
        info['height'] = g_sizeinfo_cache[src][1]
        print_color(
            "Sizeinfo hit cache: %s (%s, %s)" %
            (src, info['width'], info['height']), Color.GREEN.value)
      else:
        print_color("Trying to fetch size of " + src, Color.BLUE.value)
        size = quickQueryImgSize(src)
        if size is not None:
          info['width'] = size[0]
          info['height'] = size[1]
          g_sizeinfo_cache[src] = size
          print_color(
              "Size fetched: (%s, %s)" % (info['width'], info['height']),
              Color.BLUE.value)

      return info

  # treat src as absolute path
  if os.path.exists(src):
    print_color("Image found at local: " + src, Color.GREEN.value)
    filename = src_md5 + '.' + src.split('.')[-1]
    shutil.copyfile(src, unify_joinpath(cache_dir, filename))
    return log_and_return(filename)

  # treat src as relative path to Markdown file
  if os.path.exists(unify_joinpath(base_path, src)):
    print_color("Image found at local: " + src, Color.GREEN.value)
    filename = src_md5 + '.' + src.split('.')[-1]
    shutil.copyfile(unify_joinpath(base_path, src),
                    unify_joinpath(cache_dir, filename))
    return log_and_return(filename)

  return {"src": src, "width": -1, "height": -1}


def dump_log():
  global g_used_imgs
  global g_sizeinfo_cache

  json_path = unify_joinpath(g_conf._cache_dir, 'tmp', 'used_imgs.json')
  sizeinfo_json_path = unify_joinpath(g_conf._cache_dir, 'sizeinfo.json')

  safe_write(json_path, json.dumps(list(g_used_imgs or []), indent=1))
  safe_write(sizeinfo_json_path, json.dumps(g_sizeinfo_cache or {}, indent=1))
