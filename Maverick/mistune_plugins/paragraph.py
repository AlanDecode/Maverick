import mistune


class ParagraphRenderer(mistune.HTMLRenderer):

  def paragraph(self, text):
    # text contains figure tag
    if text.strip().startswith('<figure'):
      text = text.strip()
      if text[1:].find('<figure') > -1:
        # if there are at lease 2 figure tags
        text = [item.strip() for item in text.split('\n')]
        text = ['<div class="photos">%s</div>' % item for item in text]
        return '<div class="photoset">%s</div>' % ''.join(text)
      else:
        return text

    return '<p>%s</p>' % text
