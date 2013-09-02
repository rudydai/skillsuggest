from django.db import models

class publicSkills(models.Model):
    puburl = models.URLField()
    skills = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name
# Create your models here.
