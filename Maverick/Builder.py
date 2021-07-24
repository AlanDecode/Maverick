# -*- coding: utf-8 -*-
"""Builder

1. search source_dir recursively
2. build website structure
3. render pages
4. write to disk
"""

import functools
import os
import pathlib
import shutil
import sys

from .Config import Config
from .Content import Content, ContentList
from .Utils import (logged_func, print_color, Color, unify_joinpath,
                    force_rmtree, run)


class TemplateError(BaseException):
  pass


class Builder:

  def __init__(self, conf: Config):
    self._config = conf
    self._posts = ContentList()
    self._pages = ContentList()

  @logged_func('')
  def clean(self):
    if os.path.exists(self._config.build_dir):
      try:
        shutil.rmtree(self._config.build_dir)
      except BaseException as e:
        print(e)

  @staticmethod
  def clone_remote_theme(save_dir: str, config: dict):
    """Clone a remote repo to local disk.
    """
    os.makedirs(save_dir, exist_ok=True)

    repo_dir = os.path.join(save_dir, config['name'])

    if os.path.exists(repo_dir):
      force_rmtree(repo_dir)

    repo_url = config['url']
    repo_branch = config.get('branch', 'master')
    repo_tag = config.get('tag', '')

    def safe_run(command, cwd):
      try:
        run(command, cwd)
      except Exception:
        raise TemplateError('Cannot fetch theme from ' + repo_url)

    safe_run('git clone -b %s %s %s' % (repo_branch, repo_url, repo_dir), '.')
    if repo_tag != '':
      safe_run('git checkout %s' & repo_tag, repo_dir)

  @logged_func()
  def setup_theme(self):
    """Setup theme in this method.

    1. handle sys.path for local theme
    2. clone from remote for git theme
    3. install deps for theme
    """
    template_conf = self._config.template
    if isinstance(template_conf, str):
      # Either a local path or the name of built-in themes
      if os.path.exists(template_conf):
        template_conf = {
            'name': os.path.split(template_conf)[-1],
            'type': 'local',
            'path': template_conf
        }
      elif template_conf in ['Kepler', 'Galileo']:
        template_conf = {
            'name': template_conf,
            'type': 'git',
            'url': 'https://github.com/AlanDecode/Maverick-Theme-{}.git'.format(
                template_conf),
            'branch': 'latest'
        }
      else:
        raise TemplateError('Can not found local theme {}'.format(
            self._config.template))

    # If its remote theme, clone it to disk first
    if template_conf['type'] == 'git':
      template_path = unify_joinpath(self._config._template_dir,
                                     template_conf['name'])
      if not os.path.exists(template_path):
        self.clone_remote_theme(self._config._template_dir, template_conf)
      template_conf['type'] = 'local'
      template_conf['path'] = template_path

    sys.path.insert(0, os.path.split(template_conf['path'])[0])

    # handle deps for theme
    template_dep_file = unify_joinpath(template_conf['path'],
                                       'requirements.txt')
    if os.path.exists(template_dep_file) and os.path.isfile(template_dep_file):
      try:
        run('pip install -r %s' % template_dep_file, '.')
      except Exception:
        raise TemplateError('Can not install dependencies for theme.')

    from importlib import import_module
    self._template = import_module(template_conf['name'])

  def build_all(self):
    """Init building
        """

    # delete last build
    self.clean()

    print('Loading contents...')
    walker = os.walk(self._config.source_dir)
    source_abs_dir = pathlib.PurePath(os.path.abspath(self._config.source_dir))
    for path, _, filelist in walker:
      for file in filelist:
        if file.split(".")[-1].lower() == "md" or \
                file.split(".")[-1].lower() == "markdown":

          content_path = os.path.abspath(unify_joinpath(path, file))
          content = Content(content_path)
          if not content.get_meta("status").lower() in [
              "publish", "published", "hide", "hidden"
          ]:
            continue

          layout = content.get_meta("layout").lower()
          if layout == "post":
            if (self._config.category_by_folder):
              relative_path = pathlib.PurePath(content_path).relative_to(
                  source_abs_dir)
              relative_path = list(relative_path.parts[0:-1])
              if len(relative_path) == 0:
                relative_path.append('Default')
              content.update_meta('categories', relative_path)
            self._posts.append(content)
          elif layout == "page":
            content.update_meta('categories', [])
            self._pages.append(content)
    print('Contents loaded.')

    self._posts = ContentList(
        sorted(self._posts,
               key=functools.cmp_to_key(Content.cmp_by_date),
               reverse=True))
    self._pages = ContentList(
        sorted(self._pages,
               key=functools.cmp_to_key(Content.cmp_by_date),
               reverse=True))

    self.setup_theme()
    self._template.render(self._config, self._posts, self._pages)

    print_color('\nAll done, enjoy.', Color.GREEN.value)
