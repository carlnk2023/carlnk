from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from cars.models import CarCategory

class CarSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return CarCategory.objects.all()

    def location(self, obj):
        return reverse("single_car", args=[obj.owner.business_name_slug, obj.model_name_slug, obj.pk])

    def lastmod(self, obj):
        return obj.last_modified

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['home', 'about', 'contact', 'join']

    def location(self, item):
        return reverse(item)
