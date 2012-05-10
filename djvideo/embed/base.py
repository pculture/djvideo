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

try:
    import vidscraper
except ImportError:
    vidscraper = None
else:
    from vidscraper.suites import registry
    from vidscraper.errors import CantIdentifyUrl

from django.template import loader


class EmbedGenerator(object):

    suite = None
    template = None

    def update_context(self, context):
        pass

    def render(self, context):
        self.update_context(context)
        template = loader.get_template(self.template)
        return template.render(context)


class EmbedGeneratorRegistry(object):

    def __init__(self):
        self.suite_to_renderer = {}

    def register(self, renderer):
        if vidscraper is None:
            return
        self.suite_to_renderer[renderer.suite] = renderer

    def renderer_for_url(self, url):
        if vidscraper is None:
            return None
        if not url: # "" or None
            return None
        for suite, renderer in self.suite_to_renderer.iteritems():
            try:
                if suite.handles_video_url(url):
                    return renderer
            except NotImplementedError:
                pass
        return None

    def has_embed_generator(self, url):
        return self.renderer_for_url(url) is not None


embed_generators = EmbedGeneratorRegistry()


