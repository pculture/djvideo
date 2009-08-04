import re
from django.conf import settings
from django.template import Context, Library, Node, Variable, loader, \
    TemplateSyntaxError

register = Library()

def _get_variable_or_string(name):
    if name[0] in '"\'':
        return name[1:-1]
    else:
        return Variable(name)

ACCEPTED_KEYS = ('title', 'width', 'height', 'autoplay', 'mime_type')

DEFAULT_CONTEXT = {
    'height': 360,
    'width': 480,
    'autoplay': True,
    'settings': settings
    }

EMBED_MAPPING = {
    'video/mp4': 'quicktime.html',
    'video/quicktime': 'quicktime.html',
    'video/x-m4v': 'quicktime.html',
    'video/mpeg': 'quicktime.html',
    'video/m4v': 'quicktime.html',
    'video/mov': 'quicktime.html',
    'audio/mpeg': 'mp3.html',
    'audio/x-m4a': 'mp3.html',
    'audio/mp4': 'mp3.html',
    'video/x-mp4': 'quicktime.html',
    'audio/mp3': 'mp3.html',
    'application/x-shockwave-flash': 'flash.html',
    'video/x-flv': 'flash.html',
    'video/flv': 'flash.html',
    'application/ogg': 'videotag.html',
    'video/ogg': 'videotag.html',
    'audio/ogg': 'videotag.html',
}

YOUTUBE_VIDEO_RE = re.compile(r'http://(www.)?youtube.com/watch\?v=(?P<id>.+)')

class VideoNode(Node):
    def __init__(self, context):
        self.context = context

    def render(self, context):
        new_context = Context()
        new_context.dicts.extend(context.dicts)

        for key, value in self.context.items():
            if isinstance(value, Variable):
                new_context[key] = value.resolve(context)
            else:
                new_context[key] = value

        match = YOUTUBE_VIDEO_RE.match(new_context['url'])
        if match:
            url = 'http://www.youtube.com/v/%s&hl=en&fs=1' % match.group('id')
            new_context['url'] = url
            new_context['mime_type'] = 'video/flv'

        mime_type = new_context.get('mime_type')
        template_name = EMBED_MAPPING.get(mime_type, 'default.html')
        template = loader.get_template('djvideo/%s' % template_name)
        return template.render(new_context)


@register.tag
def video(parser, token):
    token_contents = token.split_contents()
    tag_name = token_contents[0]
    context = DEFAULT_CONTEXT.copy()
    if len(token_contents) < 2:
        raise TemplateSyntaxError(
            '%s tag requires at least one argument' % tag_name)
    context['url'] = _get_variable_or_string(token_contents[1])
    for parts in token_contents[2:]:
        name, value = parts.split('=')
        if name not in ACCEPTED_KEYS:
            raise TemplateSyntaxError(
                '%s tag does not accept the %r keyword' % (
                    tag_name, name))
        context[name.strip()] = _get_variable_or_string(value)

    return VideoNode(context)
