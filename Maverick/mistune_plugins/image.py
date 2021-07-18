# -*- coding: utf-8 -*-
"""Image
Handle cache
"""

import mistune
import os
from ..Cache import cache_img


class ImageRenderer(mistune.HTMLRenderer):
  md_path = ''
  g_hooks = {}

  def image(self, src, alt="", title=None):
    # cache image, parse its width and height
    image_meta = cache_img(src, os.path.dirname(self.md_path))
    image_meta['title'] = title
    image_meta['alt'] = alt

    def default_image(image):
      figcaption = image['title'] or image['alt'] or ''

      attr = 'data-width="%s" data-height="%s"' % (image['width'],
                                                   image['height'])

      if figcaption != "":
        figcaption = '<figcaption>%s</figcaption>' % figcaption

      return '<figure><img loading="lazy" %s src="%s" alt="%s" />%s</figure>' \
          % (attr, image['src'], image['alt'], figcaption)

    return self.g_hooks.get('output_image', default_image)(image_meta)
