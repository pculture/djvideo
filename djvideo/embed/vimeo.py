import urllib

from vidscraper.suites.vimeo import VimeoSuite

from djvideo.embed import EmbedGenerator, embed_generators


class VimeoEmbedGenerator(EmbedGenerator):

    suite = VimeoSuite()
    template = 'djvideo/embed/vimeo.html'
    supported_parameters = frozenset((
            'autoplay', 'byline', 'color', 'loop', 'portrait', 'title'))


    @classmethod
    def update_context(klass, context):
        if 'width' not in context:
            context['width'] = 400
        if 'height' not in context:
            context['height'] = 225
        match = klass.suite.video_regex.match(context['url'])
        context['video_id'] = match.group('video_id')

        # supported arguments generated w/ trial/error from
        # http://vimeo.com/21770650
        parameters = {}
        for p in klass.supported_parameters:
            if p in context:
                parameters[p] = context[p]

        if parameters:
            context['arguments'] = '?' + urllib.urlencode(parameters)
        else:
            context['arguments'] = ''


embed_generators.register(VimeoEmbedGenerator())
