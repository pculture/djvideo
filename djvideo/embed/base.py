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

from django.template import loader

from djvideo.utils import normalize_mimetype


class EmbedGenerator(object):
    #: Template which will be used to render the embed code for this
    #: generator.
    template = None
    supported_parameters = frozenset()
    default_context = {}

    def get_context(self, url, context):
        c = {
            'url': url,
            'parameters': dict((key, context[key])
                               for key in self.supported_parameters
                               if key in context)
        }
        if 'mime_type' in context:
            c['mime_type'] = normalize_mimetype(context['mime_type'])
        return c

    def generate(self, url, context):
        context.update(self.get_context(url, context))
        template = loader.get_template(self.template)
        rendered = template.render(context)
        context.pop()
        return rendered

    def handles_url(self, url):
        raise NotImplementedError


class EmbedGeneratorRegistry(object):
    def __init__(self):
        self._generators = []
        self._fallback = None

    @property
    def generators(self):
        for generator in self._generators:
            yield generator
        if self._fallback is not None:
            yield self._fallback

    def register(self, generator):
        self._generators.append(generator())

    def register_fallback(self, generator):
        self._fallback = generator()

    def get_generator(self, url):
        for generator in self.generators:
            try:
                if generator.handles_video_url(url):
                    return generator
            except NotImplementedError:
                pass
        return None


registry = EmbedGeneratorRegistry()
