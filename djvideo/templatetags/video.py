# Copyright 2009-2012 - Participatory Culture Foundation
# 
# This file is part of djvideo.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import mimetypes
import re
from django.conf import settings
from django.template import Context, Library, Node, loader, \
    TemplateSyntaxError
import simplejson

register = Library()

ACCEPTED_KEYS = ('title', 'width', 'height', 'autoplay', 'mime_type', 'poster')

DEFAULT_CONTEXT = {
    'height': 360,
    'width': 480,
    'autoplay': True,
    'settings': settings
    }

OGG_MIME_TYPES = ('application/ogg', 'video/ogg', 'audio/ogg',
                  'application/annodex', 'video/annodex', 'audio/annodex',
                  'application/x-annodex', 'video/x-annodex',
                  'audio/x-annodex', 'application/kate', 'application/x-kate',
                  'audio/vorbia', 'video/theora')

QUICKTIME_MIME_TYPES = ('video/mp4', 'video/quicktime', 'video/x-m4v',
                        'video/mpeg', 'video/m4v', 'video/mov',
                        'video/x-mp4')

H264_MIME_TYPES = ('video/h264',)

WEBM_MIME_TYPES = ('video/webm', 'audio/webm')

# supported values come (roughly) from
# http://en.wikipedia.org/wiki/Video_tag#Table
SUPPORTS_VIDEO_TAG = [
    # Firefox >= 3.1
    (re.compile('(Firefox|Shiretoko)/((3\.[1-9])|[4-9]\.|1[1-9]\.).*'),
     OGG_MIME_TYPES),
    # Firefox 4 supports WebM
    (re.compile('(Firefox|Shiretoko)/([4-9]|[1-9]{2,})\.'),
     WEBM_MIME_TYPES),
    # Chrome on Windows/OSX >= 3.0.18
    (re.compile(r'Mozilla/5.0 \([^X].+\) .* Chrome/(3\.0\.1(8[2-9]|9)|4)'),
     OGG_MIME_TYPES + QUICKTIME_MIME_TYPES),
    # Chrome everywhere, starting with 5
    (re.compile(r'Mozilla/5.0 .* Chrome/([5-9]|[1-9]{2,})\.'),
     # Chrome comes first because it also reports as Safari
     OGG_MIME_TYPES + QUICKTIME_MIME_TYPES),
    # Chrome 6 supports WebM and H264
    (re.compile(r'Mozilla/5.0 .* Chrome/([6-9]|[1-9]{2,})\.'),
     WEBM_MIME_TYPES + H264_MIME_TYPES),
    # Safari >= 526
    (re.compile(r'Mozilla/5.0 \([^X].+\) .* Safari/(52[6-9]|5[3-9][0-9])\.'),
     QUICKTIME_MIME_TYPES + H264_MIME_TYPES),
    # Internet Explorer >= 9
    (re.compile(r'Mozilla/5.0 .* MSIE (9|[1-9]{2,})\.'),
     QUICKTIME_MIME_TYPES + H264_MIME_TYPES),
    ]

EMBED_MAPPING = {
    'video/mp4': 'quicktime.html',
    'video/quicktime': 'quicktime.html',
    'video/x-m4v': 'quicktime.html',
    'video/mpeg': 'quicktime.html',
    'video/m4v': 'quicktime.html',
    'video/mov': 'quicktime.html',
    'video/x-mp4': 'quicktime.html',
    'application/x-shockwave-flash': 'flash.html',
    'video/x-flv': 'flash.html',
    'video/flv': 'flash.html',
}

if getattr(settings, 'XSPF_PLAYER_URL', False):
    EMBED_MAPPING.update({
    'audio/mpeg': 'mp3.html',
    'audio/x-m4a': 'mp3.html',
    'audio/mp4': 'mp3.html',
    'audio/mp3': 'mp3.html',
    })

YOUTUBE_VIDEO_RE = re.compile(r'http://(www.)?youtube.com/watch\?v=(?P<id>.+)')

class VideoNode(Node):
    def __init__(self, context):
        self.context = context

    def render(self, context):
        new_context = Context()
        new_context.dicts.extend(context.dicts)

        for key, value in self.context.items():
            # some things in the context (defaults) are not Varibles, so don't
            # convert them.
            if hasattr(value, 'resolve'):
                new_context[key] = value.resolve(context)
            else:
                new_context[key] = value

        match = YOUTUBE_VIDEO_RE.match(new_context['url'])
        if match:
            url = 'http://www.youtube.com/v/%s&hl=en&fs=1' % match.group('id')
            new_context['url'] = url
            new_context['mime_type'] = 'video/flv'

        mime_type = new_context.get('mime_type')
        if not mime_type:
            mime_type, _ = mimetypes.guess_type(new_context['url'])
            new_context['mime_type'] = mime_type
        new_context['hash'] = hash(new_context)
        template_name = EMBED_MAPPING.get(mime_type, 'default.html')
        template = loader.get_template('djvideo/%s' % template_name)
        rendered = template.render(new_context)
        user_agent = context['request'].META.get('HTTP_USER_AGENT')
        if user_agent:
            for regexp, mime_types in SUPPORTS_VIDEO_TAG:
                if mime_type in mime_types:
                    if regexp.search(user_agent):
                        if regexp != SUPPORTS_VIDEO_TAG[0][0]:
                            # Firefox renders the <obect> fallback tag, causing
                            # the audio to play twice (Bug #487398)
                            new_context['fallback'] = rendered
                        template = loader.get_template('djvideo/videotag.html')
                        return template.render(new_context)
        return rendered


@register.tag
def video(parser, token):
    token_contents = token.split_contents()
    tag_name = token_contents[0]
    context = DEFAULT_CONTEXT.copy()
    if len(token_contents) < 2:
        raise TemplateSyntaxError(
            '%s tag requires at least one argument' % tag_name)
    context['url'] =  parser.compile_filter(token_contents[1])
    for parts in token_contents[2:]:
        name, value = parts.split('=')
        if name not in ACCEPTED_KEYS:
            raise TemplateSyntaxError(
                '%s tag does not accept the %r keyword' % (
                    tag_name, name))
        context[name.strip()] = parser.compile_filter(value)

    return VideoNode(context)


@register.filter
def is_ogg_media(mime_type):
    return mime_type in OGG_MIME_TYPES

@register.filter
def is_quicktime_media(mime_type):
    return mime_type in QUICKTIME_MIME_TYPES

@register.filter
def is_h264_media(mime_type):
    return mime_type in H264_MIME_TYPES

@register.filter
def is_webm_media(mime_type):
    return mime_type in WEBM_MIME_TYPES
