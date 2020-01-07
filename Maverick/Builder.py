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

from .Utils import logged_func, print_color, Color, unify_joinpath, force_rmtree, run
from .Content import Content, ContentList
from .Config import Config


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

    @logged_func()
    def setup_theme(self):
        """Setup theme in this method.

        1. handle sys.path for local theme
        2. clone from remote for git theme
        3. install deps for theme
        """
        template = ''
        template_dep_file = ''
        mvrk_path = self._config.mvrk_path

        def clone_remote_theme(config: dict):
            repo_dir = os.path.abspath(mvrk_path + '/Templates/' + config['name'])
            if os.path.exists(repo_dir):
                force_rmtree(repo_dir)

            repo_url = config['url']
            repo_branch = config.get('branch', 'master')
            repo_tag = config.get('tag', '')

            def safe_run(command, cwd):
                try:
                    run(command, cwd)
                except:
                    raise TemplateError('Cannot fetch theme from '+repo_url)

            safe_run('git clone -b %s %s %s' %
                     (repo_branch, repo_url, repo_dir), mvrk_path)
            if repo_tag != '':
                safe_run('git checkout %s' & repo_tag, repo_dir)

        if type(self._config.template) == str:
            """check for local theme, handle fallback for Galileo and Kepler,
            since they are built-in themes.
            """
            built_in_themes = ['Kepler', 'Galileo']
            if not os.path.exists(unify_joinpath(mvrk_path + '/Templates', self._config.template)):
                if self._config.template in built_in_themes:
                    clone_remote_theme({
                        "name": self._config.template,
                        "type": "git",
                        "url": "https://github.com/AlanDecode/Maverick-Theme-%s.git" % self._config.template,
                        "branch": "latest"
                    })
                    template = '.'.join(['Templates', self._config.template])
                    template_dep_file = mvrk_path + '/Templates/%s/requirements.txt' % self._config.template
                else:
                    raise TemplateError(
                        'Can not found local theme '+self._config.template)
            else:
                template = '.'.join(['Templates', self._config.template])
                template_dep_file = mvrk_path + '/Templates/%s/requirements.txt' % self._config.template

        elif type(self._config.template) == dict:
            if self._config.template['type'] == 'local':
                local_dir = os.path.abspath(self._config.template['path'])
                if not os.path.exists(local_dir):
                    raise TemplateError(
                        'Can not found local theme '+self._config.template['name'])
                else:
                    sys.path.insert(0, os.path.dirname(local_dir))
                    template = self._config.template['name']
                    template_dep_file = unify_joinpath(
                        local_dir, 'requirements.txt')
            elif self._config.template['type'] == 'git':
                clone_remote_theme(self._config.template)
                template = '.'.join(
                    ['Templates', self._config.template['name']])
                template_dep_file = mvrk_path + '/Templates/%s/requirements.txt' % self._config.template['name']

        else:
            raise TemplateError('Invalid template config',
                                str(self._config.template))

        # handle deps for theme
        if os.path.exists(template_dep_file) and os.path.isfile(template_dep_file):
            try:
                run('pip install -r %s' % template_dep_file, '.')
            except:
                raise TemplateError('Can not install dependencies for theme.')

        from importlib import import_module
        self._template = import_module(template)

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

        self.setup_theme()
        self._template.render(self._config, self._posts, self._pages)

        print_color('\nAll done, enjoy.', Color.GREEN.value)
