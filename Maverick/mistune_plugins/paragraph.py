import mistune


class ParagraphRenderer(mistune.HTMLRenderer):
    def paragraph(self, text):
        if text.strip().startswith('<figure'):
            text = [item.strip() for item in text.strip().split('\n')]
            text = ['<div class="photos">%s</div>' % item for item in text]
            return '<div class="photoset">%s</div>' % ''.join(text)
        else:
            return '<p>%s</p>' % text
