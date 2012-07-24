import re
import urllib

from vidscraper.suites.youtube import YouTubeSuite

from djvideo.embed import EmbedGenerator, registry


YOUTUBE_RE = re.compile(YouTubeSuite.video_regex)


class YouTubeEmbedGenerator(EmbedGenerator):
    template = 'djvideo/embed/youtube.html'
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
        match = YOUTUBE_RE.match(url)
        c['video_id'] = match.group('video_id')
        return c


registry.register(YouTubeEmbedGenerator, YouTubeSuite)
