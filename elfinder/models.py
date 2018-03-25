from django.db import models
from elfinder.fields import ElfinderField 

class YawdElfinderTestModel(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    anyfile = ElfinderField(help_text='This is the default configuration')
    image = ElfinderField(optionset='image',
                          help_text='This field uses the "image" optionset')
    pdf = ElfinderField(optionset='pdf', blank=True, null=True,
                        help_text='This field uses the "pdf" custom optionset, ' \
                        'set in the project settings file')
    
    def __unicode__(self):
        return self.name