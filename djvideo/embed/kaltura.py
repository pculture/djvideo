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

import re

from vidscraper.exceptions import UnhandledVideo

from djvideo.embed import EmbedGenerator, registry


class KalturaEmbedGenerator(EmbedGenerator):
    path_re = re.compile(r'^https?://cdnsecakmi.kaltura.com/p/'
                         r'(?P<partner_id>[\d]+)/sp/(?P<subp_id>[\d]+)'
                         r'/flvclipper/entry_id/(?P<entry_id>[\w]+)/'
                         r'version/0(?:/ext/flv)?')
    template = 'djvideo/kaltura.html'
    default_context = {'width': 459, 'height': 344}

    def get_url_data(self, url):
        match = self.path_re.match(url)
        if match:
            return match.groupdict()
        raise UnhandledVideo(url)

    def get_context(self, url, context):
        c = super(KalturaEmbedGenerator, self).get_context(url, context)
        c.update(self.get_url_data(url))
        return c

    def handles_video_url(self, url):
        try:
            self.get_url_data(url)
        except UnhandledVideo:
            return False
        return True


registry.register(KalturaEmbedGenerator)
