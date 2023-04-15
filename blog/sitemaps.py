from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSitemap(Sitemap):
    changefreg = 'weekly'
    priority = 0.9

    def items(self):
        """returns queryset"""
        return Post.published.all()

    def lastmod(self, obj):
        """returns the time the object was last modified"""
        return obj.updated
