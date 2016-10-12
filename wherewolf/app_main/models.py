from django.db import models

# database table abstractions
# Managers deal with functions at the table level
# individual model instances represent a table row


class Area(models.Model):

    name = models.TextField(blank=True, null=True, max_length=100)

    geo_lat = models.FloatField(null=True)
    geo_long = models.FloatField(null=True)


class Place(models.Model):

    name = models.TextField(blank=True, null=True, max_length=100)
    area = models.ForeignKey(Area)

    geo_lat = models.FloatField(null=True)
    geo_long = models.FloatField(null=True)


class FeatureManager(models.Manager):

    def get_latest(self):
        return super(FeatureManager, self).all()[:10]



class Feature(models.Model):

    place = models.ForeignKey(Place)

    category = models.TextField(blank=True, null=True, max_length=254)
    name = models.TextField(blank=True, null=True, max_length=254)
    description1 = models.TextField(blank=True, null=True)
    description2 = models.TextField(blank=True, null=True)
    image = models.ImageField()

    date_feature = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_expires = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    company = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)

    geo_lat = models.FloatField(null=True)
    geo_long = models.FloatField(null=True)

    objects = FeatureManager()

