from django.contrib import sitemaps
from datetime import datetime
from core.client.models import Room

class AbstractSitemapClass():
    changefreq = 'daily'
    url = None

    def get_absolute_url(self):
        return self.url


class StaticSitemap(sitemaps.Sitemap):
    protocol = 'https'
    pages = {'home': '/', 'about': '/about/',
             'get-started': '/get-started/',
             'register': '/accounts/register/',
             'login': '/accounts/login/',
             'rooms': '/rooms/'
             }
    main_sitemaps = []
    for page in pages.keys():
        sitemap_class = AbstractSitemapClass()
        sitemap_class.url = pages[page]
        main_sitemaps.append(sitemap_class)

    def items(self):
        return self.main_sitemaps

    lastmod = datetime(2013, 01, 06)
    priority = 1
    changefreq = "yearly"


class GenericSitemap(sitemaps.GenericSitemap):
    protocol = 'https'
    room_info_dict = {
                      'queryset': Room.objects.all(),
                      'date_field': 'created_date',
    }    
    def __init__(self):
        super(GenericSitemap, self).__init__(self.room_info_dict, changefreq='Daily')
    
