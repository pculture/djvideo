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

from vidscraper.exceptions import UnhandledVideo
from vidscraper.suites.vimeo import PathMixin

from djvideo.embed import EmbedGenerator, registry


class VimeoEmbedGenerator(PathMixin, EmbedGenerator):
    template = 'djvideo/embed/vimeo.html'
    # supported arguments generated w/ trial/error from
    # http://vimeo.com/21770650
    supported_parameters = frozenset((
            'autoplay', 'byline', 'color', 'loop', 'portrait', 'title'))
    default_context = {'width': 400, 'height': 225}

    def get_context(self, url, context):
        c = super(VimeoEmbedGenerator, self).get_context(url, context)
        c.update(self.get_url_data(url))
        return c

    def handles_video_url(self, url):
        try:
            self.get_url_data(url)
        except UnhandledVideo:
            return False
        return True


registry.register(VimeoEmbedGenerator)
