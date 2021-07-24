# -*- coding: utf-8 -*-
import moment

from .Config import g_conf


class Metadata(dict):
  """Metadata

    文章以及页面的元数据
    """

  def __init__(self, fr):
    dict.__init__({})
    self["title"] = str(fr.get("title", ""))
    self["slug"] = str(fr.get("slug", self["title"]))
    self["date"] = moment.date(str(fr.get("date", ""))).locale(g_conf.locale)
    self["layout"] = str(fr.get("layout", "post"))
    self["status"] = str(fr.get("status", "publish"))
    self["author"] = str(fr.get("author", ""))
    self["banner"] = str(fr.get("banner", ""))
    self["excerpt"] = str(fr.get("excerpt", ""))
    self["path"] = ""
    self["showfull"] = bool(fr.get("showfull", False))
    self["comment"] = bool(fr.get("comment", True))

    # 解析包含的 tag（无序）
    self["tags"] = fr.get("tags", []) or []

    # 解析包含的类别（有序）
    self["categories"] = fr.get("categories", []) or []
    if len(self["categories"]) == 0:
      self["categories"].append('Default')
