from django.contrib.gis.db import models

class Location(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    point = models.PointField(srid=4326)  
    address = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    @property
    def latitude(self):
        return self.point.y

    @property
    def longitude(self):
        return self.point.x