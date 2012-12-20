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

from vidscraper.suites.youtube import YouTubeSuite

from djvideo.embed import EmbedGenerator, registry


class YouTubeEmbedGenerator(EmbedGenerator):
    suite = YouTubeSuite()
    template = 'djvideo/youtube.html'
    # supported arguments listed at
    # https://developers.google.com/youtube/player_parameters#Parameters
    supported_parameters = frozenset((
            'autohide', 'autoplay', 'cc_load_policy', 'color', 'controls',
            'disablekb', 'enablejsapi', 'fs', 'iv_load_policy', 'list',
            'listType', 'loop', 'modestbranding', 'origin', 'playerapiid',
            'playlist', 'rel', 'showinfo', 'start', 'theme'))
    default_context = {'width': 459, 'height': 344}

    def get_context(self, url, context):
        c = super(YouTubeEmbedGenerator, self).get_context(url, context)
        match = self.suite.video_regex.match(url)
        c['video_id'] = match.group('video_id')
        return c

    def handles_video_url(self, url):
        return self.suite.handles_video_url(url)


registry.register(YouTubeEmbedGenerator)
