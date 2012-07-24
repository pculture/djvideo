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
from django.template import Library, Node, loader, TemplateSyntaxError
from django.template.base import kwarg_re

from djvideo.utils import normalize_mimetype

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
    def __init__(self, url, kwargs):
        self.url = url
        self.kwargs = kwargs

    def render(self, context):
        url = self.url.resolve(context)
        # pushes a new dict into the context.
        kwargs = dict((key, value.resolve(context))
                       for key, value in self.kwargs.iteritems())
        context.update(kwargs)
        context['url'] = url

        match = YOUTUBE_VIDEO_RE.match(context['url'])
        if match:
            url = 'http://www.youtube.com/v/%s&hl=en&fs=1' % match.group('id')
            context['url'] = url
            context['mime_type'] = 'video/flv'

        mime_type = context.get('mime_type')
        if not mime_type:
            mime_type, _ = mimetypes.guess_type(context['url'])
            context['mime_type'] = mime_type
        context['hash'] = hash(context)
        if mime_type:
            mime_type = normalize_mimetype(mime_type)
            context['mime_type'] = mime_type
        template_name = EMBED_MAPPING.get(mime_type, 'default.html')
        template = loader.get_template('djvideo/%s' % template_name)
        context['fallback'] = template.render(context)
        template = loader.get_template('djvideo/videotag.html')
        rendered = template.render(context)
        context.pop()
        return rendered


@register.tag
def video(parser, token):
    bits = token.split_contents()
    tag_name = bits[0]

    if len(bits) < 2:
        raise TemplateSyntaxError(
            '%s tag requires at least one argument' % tag_name)

    url = parser.compile_filter(bits[1])
    kwargs = DEFAULT_CONTEXT.copy()

    bits = bits[2:]

    for bit in bits:
        match = kwarg_re.match(bit)
        if not match:
            raise TemplateSyntaxError(
                    'Malformed arguments to {0} tag.'.format(tag_name))
        key, value = match.groups()
        if key:
            if key not in ACCEPTED_KEYS:
                raise TemplateSyntaxError(
                    '{0} tag does not accept the {1} keyword'.format(
                        tag_name, key))
            kwargs[key] = parser.compile_filter(value)
        else:
            raise TemplateSyntaxError('{0} tag only takes one positional '
                                      'argument.'.format(tag_name))

    return VideoNode(url, kwargs)


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
