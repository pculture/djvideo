import urllib

from vidscraper.suites.vimeo import VimeoSuite

from djvideo.embed import EmbedGenerator, registry


class VimeoEmbedGenerator(EmbedGenerator):
    template = 'djvideo/embed/vimeo.html'
    # supported arguments generated w/ trial/error from
    # http://vimeo.com/21770650
    supported_parameters = frozenset((
            'autoplay', 'byline', 'color', 'loop', 'portrait', 'title'))
    default_context = {'width': 400, 'height': 225}

    def get_context(self, url, context):
        c = super(VimeoEmbedGenerator, self).get_context(url, context)
        match = VimeoSuite.video_regex.match(url)
        c['video_id'] = match.group('video_id')
        return c


registry.register(VimeoEmbedGenerator, VimeoSuite)
