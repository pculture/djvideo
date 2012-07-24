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

import warnings

from django.template import Library

from djvideo.templatetags.generate_embed import generate_embed

register = Library()


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


@register.tag
def video(parser, token):
    warnings.warn("{% video %} tag is deprecated. Use {% generate_embed %} "
                  "instead.")
    return generate_embed(parser, token)


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
