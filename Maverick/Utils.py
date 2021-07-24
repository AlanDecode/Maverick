# -*- coding: utf-8 -*-

import os
import re
import shutil
import codecs
import hashlib
import stat
import subprocess
from enum import Enum

import chardet

from .Config import g_conf
from .Router import Router


class Color(Enum):
  BLACK = 30
  RED = 31
  GREEN = 32
  YELLOW = 33
  BLUE = 34
  MAGENTA = 35
  CYAN = 36
  WHITE = 37


def print_color(text: str, fg: Color = Color.BLACK.value, end='\n'):
  print('\033[%sm%s\033[0m' % (fg, text), end=end)


def run(command, cwd):
  with subprocess.Popen(command, cwd=cwd, shell=True) as ret:
    ret.wait()
    if ret.returncode != 0:
      ret.kill()
      raise BaseException


def logged_func(delim='\n'):

  def inner(func):

    def wrapper(*args, **kwargs):
      log_start(func.__name__, delim)
      func(*args, **kwargs)
      log_end()

    return wrapper

  return inner


def copytree(src, dst, syamlinks=False, ignore=None):
  for item in os.listdir(src):
    s = unify_joinpath(src, item)
    d = unify_joinpath(dst, item)
    if os.path.isdir(s):
      shutil.copytree(s, d, syamlinks, ignore)
    else:
      shutil.copy2(s, d)


def force_rmtree(top):
  for root, dirs, files in os.walk(top, topdown=False):
    for name in files:
      filename = os.path.join(root, name)
      os.chmod(filename, stat.S_IWUSR)
      os.remove(filename)
    for name in dirs:
      os.rmdir(os.path.join(root, name))
  os.rmdir(top)


def log_start(message, delim):
  print_color('Start ' + message, Color.YELLOW.value, end='...' + delim)


def log_end():
  print_color('done.', Color.YELLOW.value)


def safe_write(path, content, codec="utf-8"):
  if not os.path.exists(os.path.dirname(path)):
    os.makedirs(os.path.dirname(path))

  with codecs.open(path, "w+", encoding=codec) as f:
    f.write(content)


def safe_read(path):
  if not os.path.exists(path):
    return ""

  # utf-8 is prefered
  try:
    with open(path, 'r', encoding='utf-8') as f:
      return f.read()
  except UnicodeDecodeError:
    with open(path, 'rb') as f:
      content = f.read()
      encoding = chardet.detect(content)['encoding'] or 'utf-8'
      return content.decode(encoding=encoding)


def gen_hash(str):
  h1 = hashlib.md5()
  h1.update(str.encode(encoding='utf-8'))
  return h1.hexdigest()


def unify_joinpath(left, right, *args):
  path = os.path.join(left, right, *args)
  return path.replace('\\', '/')


def filterPlaceholders(content):
  """replace content like ${key} to corresponding value

    1. search key in env
    2. search key in config
    """
  pattern = re.compile(r'[\s\S]*?\$\{([\s\S]*?)\}')
  router = Router(g_conf)

  def getKey(str):
    m = pattern.match(str)
    if m is not None:
      return m.group(1)
    else:
      return None

  while True:
    key = getKey(content)
    if key is None:
      break

    search_str = '${%s}' % key
    value = ''
    if key == "static_prefix":
      value = router.gen_static_file_prefix()
    else:
      # find in os.env
      value = os.getenv(key, None)
      if value is None:
        # find in config
        try:
          value = getattr(g_conf, key)
        except AttributeError:
          pass

    # replace
    content = content.replace(search_str, str(value), 1)

  return content
