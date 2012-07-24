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

import mimetypes

from djvideo.embed import EmbedGenerator, registry
from djvideo.utils import normalize_mimetype


#: Mimetypes which should use the quicktime template.
QUICKTIME_MIMETYPES = frozenset(('video/mp4', 'video/quicktime',
                                 'video/x-m4v', 'video/mpeg', 'video/m4v',
                                 'video/mov', 'video/x-mp4'))

#: Mimetypes which should use the flash template.
FLASH_MIMETYPES = frozenset(('application/x-shockwave-flash', 'video/x-flv',
                             'video/flv'))


class FileEmbedGenerator(EmbedGenerator):
    """
    FileEmbedGenerator handles the generic case of embedding files that aren't
    picked up by any other embed generators.

    """
    template = 'djvideo/files/base.html'
    default_context = {
        'height': 360,
        'width': 480,
        'autoplay': True,
    }
    supported_parameters = frozenset(('title', 'width', 'height', 'autoplay',
                                      'mime_type', 'poster'))

    def get_context(self, url, context):
        c = super(FileEmbedGenerator, self).get_context(url, context)
        mime_type = context.get('mime_type')
        if not mime_type:
            mime_type = mimetypes.guess_type(url, strict=False)[0]
        mime_type = normalize_mimetype(mime_type)
        c['mime_type'] = mime_type
        if mime_type in QUICKTIME_MIMETYPES:
            c['fallback_template'] = 'djvideo/files/quicktime.html'
        elif mime_type in FLASH_MIMETYPES:
            c['fallback_template'] = 'djvideo/files/flash.html'
        else:
            c['fallback_template'] = 'djvideo/files/default.html'
        return c

    def handles_video_url(self, url):
        return True


registry.register_fallback(FileEmbedGenerator)
