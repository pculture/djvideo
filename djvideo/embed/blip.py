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

from bs4 import BeautifulSoup
from vidscraper.suites.blip import Suite

from djvideo.embed import EmbedGenerator, registry


class BlipEmbedGenerator(EmbedGenerator):
    suite = Suite()
    template = 'djvideo/blip.html'
    supported_parameters = frozenset()
    default_context = {'width': 550, 'height': 443}

    def get_context(self, url, context):
        c = super(BlipEmbedGenerator, self).get_context(url, context)
        embed_code = context['current_video'].embed_code
        soup = BeautifulSoup(embed_code)
        try:
            video_id = soup.embed['src'].rsplit("#", 1)[1]
        except (KeyError, TypeError, AttributeError, IndexError):
            video_id = ''
        c['video_id'] = video_id
        return c

    def handles_video_url(self, url):
        return self.suite.handles_video(url)


registry.register(BlipEmbedGenerator)
