from django.contrib.sitemaps import Sitemap
from datetime import datetime


class AbstractSitemapClass():
    changefreq = 'daily'
    url = None

    def get_absolute_url(self):
        return self.url


class StaticSitemap(Sitemap):
    pages = {'home': '/'}
    main_sitemaps = []
    for page in pages.keys():
        sitemap_class = AbstractSitemapClass()
        sitemap_class.url = pages[page]
        main_sitemaps.append(sitemap_class)

    def items(self):
        return self.main_sitemaps
    lastmod = datetime(2012, 12, 02)
    priority = 1
    changefreq = "yearly"
