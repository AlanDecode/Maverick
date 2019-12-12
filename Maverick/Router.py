# -*- coding: utf-8 -*-


class Router:
    def __init__(self, conf):
        """Create permalink for a content.
        """
        self.config = conf

    def gen_permalink_by_meta(self, meta):
        link, _ = self.gen_by_meta(meta)
        return link

    def gen_permalink_by_content(self, content):
        link, _ = self.gen_by_content(content)
        return link

    def gen_permalink(self, type, slug, page=0):
        link, _ = self.gen(type, slug, page)
        return link

    def gen_by_meta(self, meta):
        return self.gen(meta["layout"], meta["slug"])

    def gen_by_content(self, content):
        return self.gen(content.get_meta('layout'), content.get_meta('slug'))

    def gen(self, type, slug, page=1):
        routes = list()
        if type == "post":
            routes = ["archives", slug]
        elif type == "page":
            routes = [slug]
        elif type == "tag" or type == "category":
            routes = [type, slug]
        elif type == "archives":
            routes = ["archives"]
        elif type == "index" and page > 1:
            routes = ["page"]

        if page > 1:
            routes.append(str(page))

        path = "/".join(routes)
        if len(routes):
            path += "/"

        local_path = self.config.build_dir + path
        permalink = self.config.site_prefix + path

        return permalink, local_path
