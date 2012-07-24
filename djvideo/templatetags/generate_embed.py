# Copyright 2012 - Participatory Culture Foundation
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

from django.template import Library, TemplateSyntaxError, Node
from django.template.base import kwarg_re

from djvideo.embed import embed_generators
from djvideo.templatetags.video import VideoNode, DEFAULT_CONTEXT
from djvideo.utils import normalize_mimetype


register = Library()


class EmbedGeneratorNode(Node):
    def __init__(self, url, kwargs):
        self.url = url
        self.kwargs = kwargs

    def render(self, context):
        url = self.url.resolve(context)
        renderer = embed_generators.renderer_for_url(url)

        if renderer is None:
            context.update(DEFAULT_CONTEXT)
            renderer = VideoNode({})

        # pushes a new dict into the context.
        kwargs = dict((key, value.resolve(context))
                       for key, value in self.kwargs.iteritems())
        context.update(kwargs)
        context['url'] = url

        if 'mime_type' in context:
            context['mime_type'] = normalize_mimetype(context['mime_type'])

        rendered = renderer.render(context)

        context.pop()

        if isinstance(renderer, VideoNode):
            context.pop()
        return rendered


@register.filter
def has_embed_generator(url):
    return embed_generators.has_embed_generator(url)


@register.tag
def generate_embed(parser, token):
    """
    Includes a template suitable for generating embed code for the given url.
    Additional kwargs may be supplied, which will be passed on as parameters
    for embedding - for example, autoplay values.

        {% generate_embed "http://www.youtube.com/watch?v=J_DV9b0x7v4" autoplay=1 %}

    """
    bits = token.split_contents()
    tag_name = bits[0]
    if len(bits) < 2:
        raise TemplateSyntaxError(
            '{0} tag requires at least 1 argument'.format(tag_name))

    url = parser.compile_filter(bits[1])
    kwargs = {}

    bits = bits[2:]

    for bit in bits:
        match = kwarg_re.match(bit)
        if not match:
            raise TemplateSyntaxError(
                    'Malformed arguments to {0} tag.'.format(tag_name))
        key, value = match.groups()
        if key:
            kwargs[key] = parser.compile_filter(value)
        else:
            raise TemplateSyntaxError('{0} tag only takes one positional '
                                      'argument.'.format(tag_name))
    return EmbedGeneratorNode(url, kwargs)
