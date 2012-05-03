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


from django.template import (Library, TemplateSyntaxError, Node, Context,
                             Variable)

from djvideo.utils import get_variable_or_string
from djvideo.embed import embed_generators
from djvideo.templatetags.video import VideoNode, DEFAULT_CONTEXT


register = Library()


class EmbedGeneratorNode(Node):
    def __init__(self, arguments):
        self.arguments = arguments

    def render(self, context):
        new_context = Context()
        new_context.dicts.extend(context.dicts)
        for key, value in self.arguments.iteritems():
            if isinstance(value, Variable):
                new_context[key] = value.resolve(context)
            else:
                new_context[key] = value

        renderer = embed_generators.renderer_for_url(new_context['url'])
        if renderer is None:
            video_context = Context()
            video_context.dicts.extend(DEFAULT_CONTEXT)
            video_context.dicts.extend(new_context)
            node = VideoNode({})
            return node.render(video_context)
        return renderer.render(new_context)


@register.filter
def host_supports_embed_generation(url):
    return embed_generators.supports_embed_generation(url)


@register.tag
def generate_embed(parser, token):
    token_contents = token.split_contents()
    tag_name = token_contents[0]
    if len(token_contents) < 2:
        raise TemplateSyntaxError(
            '%s tag requires at least 1 argument' % tag_name)
    arguments = {
        'url': get_variable_or_string(token_contents[1])
        }
    for kwarg in token_contents[2:]:
        if '=' not in kwarg:
            raise TemplateSyntaxError(
                '%s tag does not take more than 1 positional argument: %r' % (
                    tag_name, kwarg))
        key, value = kwarg.split('=', 1)
        arguments[key.strip()] = get_variable_or_string(value)

    return EmbedGeneratorNode(arguments)
