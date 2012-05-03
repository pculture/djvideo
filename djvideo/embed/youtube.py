import urllib

from vidscraper.suites.youtube import YouTubeSuite

from djvideo.embed import EmbedGenerator, embed_generators


class YouTubeEmbedGenerator(EmbedGenerator):

    suite = YouTubeSuite()
    template = 'djvideo/embed/youtube.html'
    supported_parameters = frozenset((
            'autohide', 'autoplay', 'cc_load_policy', 'color', 'controls',
            'disablekb', 'enablejsapi', 'fs', 'iv_load_policy', 'list',
            'listType', 'loop', 'modestbranding', 'origin', 'playerapiid',
            'playlist', 'rel', 'showinfo', 'start', 'theme'))

    @classmethod
    def update_context(klass, context):
        if 'width' not in context:
            context['width'] = 459
        if 'height' not in context:
            context['height'] = 344
        match = klass.suite.video_regex.match(context['url'])
        context['video_id'] = match.group('video_id')

        # supported arguments listed at
        # https://developers.google.com/youtube/player_parameters#Parameters
        parameters = {}
        for p in klass.supported_parameters:
            if p in context:
                parameters[p] = context[p]

        if parameters:
            context['arguments'] = '?' + urllib.urlencode(parameters)
        else:
            context['arguments'] = ''


embed_generators.register(YouTubeEmbedGenerator())
