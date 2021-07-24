# -*- coding: utf-8 -*-
import re
import yaml

from .Metadata import Metadata
from .Markdown import Markdown
from .Utils import safe_read


def group_by_tagname(tag):

  def criteria(content):
    return tag in content.get_meta('tags')

  return criteria


def group_by_category(category):

  def criteria(content):
    # direct category
    return category == content.get_meta('categories')[-1]

  return criteria


class Content():

  def __init__(self, path):
    content = safe_read(path)

    # parse frontmatter
    r = re.compile(r'---([\s\S]*?)---')
    m = r.match(content)

    self.meta = Metadata(yaml.safe_load(m.group(1)))
    self.meta['path'] = path
    self.text = content[len(m.group(0)):]

    self.skip = not self.get_meta('status').lower() in ["publish", "published"]

    self._parsed = None
    self._excerpt = None

  @property
  def excerpt(self):
    if self._excerpt is None:

      def strip(text):
        r = re.compile(r'<[^>]+>', re.S)
        return r.sub('', text)

      output = self.get_meta("excerpt")
      if output != "" and output != "None":
        return output

      # find <!--more-->
      index = self.parsed.find('<!--more-->')
      if index != -1:
        output = strip(self.parsed[:index])
      else:
        output = strip(self.parsed)
        output = output[:output.find('\n')]
      self._excerpt = output

    return self._excerpt

  @property
  def parsed(self):
    if self._parsed is None:
      self._parsed = Markdown(self)
    return self._parsed

  def get_meta(self, key, default=None):
    return self.meta.get(key, default)

  def update_meta(self, key, value):
    self.meta[key] = value

  @staticmethod
  def cmp_by_date(content_1, content_2):
    date_1 = content_1.get_meta('date')
    date_2 = content_2.get_meta('date')
    if date_1 < date_2:
      return -1
    elif date_1 > date_2:
      return 1
    else:
      return 0


class ContentList(list):
  """Content List.

    Convinient for sorting and slicing.
    """

  def __init__(self, from_obj=[]):
    list.__init__(self, from_obj)

  def re_group(self, _func):
    """subset items with _func(item) = True
        """
    resultList = ContentList()
    for meta in self:
      if _func(meta) is True:
        resultList.append(meta)
    return resultList
