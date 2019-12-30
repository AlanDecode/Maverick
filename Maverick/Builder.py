# -*- coding: utf-8 -*-
"""Builder

1. search source_dir recursively
2. build website structure
3. render pages
4. write to disk
"""

import os
import sys
import shutil
import functools
import pathlib

from .Utils import logged_func, print_color, Color, unify_joinpath
from .Content import Content, ContentList
from .Config import Config


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

    def build_all(self):
        """Init building
        """

        # delete last build
        self.clean()

        print('Loading contents...')
        walker = os.walk(self._config.source_dir)
        source_abs_dir = pathlib.PurePath(
            os.path.abspath(self._config.source_dir))
        for path, _, filelist in walker:
            for file in filelist:
                if file.split(".")[-1].lower() == "md" or \
                        file.split(".")[-1].lower() == "markdown":

                        content_path = os.path.abspath(
                            unify_joinpath(path, file))
                        content = Content(content_path)
                        if not content.get_meta("status").lower() in [
                                "publish", "published", "hide", "hidden"]:
                            continue

                        layout = content.get_meta("layout").lower()
                        if layout == "post":
                            if (self._config.category_by_folder):
                                relative_path = pathlib.PurePath(
                                    content_path).relative_to(source_abs_dir)
                                relative_path = list(relative_path.parts[0:-1])
                                if len(relative_path) == 0:
                                    relative_path.append('Default')
                                content.update_meta(
                                    'categories', relative_path)
                            self._posts.append(content)
                        elif layout == "page":
                            content.update_meta('categories', [])
                            self._pages.append(content)
        print('Contents loaded.')

        self._posts = ContentList(sorted(self._posts,
                                         key=functools.cmp_to_key(
                                             Content.cmp_by_date),
                                         reverse=True))
        self._pages = ContentList(sorted(self._pages,
                                         key=functools.cmp_to_key(
                                             Content.cmp_by_date),
                                         reverse=True))

        # render all by template
        template = ''
        if type(self._config.template) == str:
            template = ".".join(["Templates", self._config.template])
        elif type(self._config.template) == dict:
            if self._config.template['type'] == 'local':
                sys.path.append(os.path.dirname(
                    os.path.abspath(self._config.template['path'])))
                template = self._config.template['name']
        else:
            template = 'Templates.Galileo'

        from importlib import import_module
        template = import_module(template)
        template.render(self._config, self._posts, self._pages)

        print_color('\nAll done, enjoy.', Color.GREEN.value)
