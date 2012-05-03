# djvideo #

## About ##

This is a Django Video module.  It allows you to embed video files, as well as
players from YouTube and Vimeo.

## Code ##
Code is at:

    https://github.com/pculture/djvideo

License information is in the LICENSE file.

## Usage ##

Embedding a video file directly:

```
{% load video %}
{% video [variable or string with the video file] [width] [height] %}
{% if video.url|is_ogg_media %}Here's a message about Ogg Video!{% endif %}
```

Embedding a YouTube/Vimeo player:

```
{% load generate_embed %}
{% if video.website_url|supports_embed_generation %}
{% generate_embed video.website_url width=1024 height=767 autoplay=1 %}
{% else %}
Do something else! We couldn't generate any embed code.
{% endif %}
```
