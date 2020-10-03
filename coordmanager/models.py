from django.db import models
from django.utils.translation import gettext_lazy as _

class Coordinate(models.Model):
    """
    Stores coordinates points
    """
    x = models.FloatField(help_text=_("longitude"))
    y = models.FloatField(help_text=_("latitude"))

    class Meta:
        verbose_name = _("coordinate")
        verbose_name_plural = _("coordinates")

    def __str__(self):
        return 'coordinate(id=%s, x=%s, y=%s)' % (self.id, self.x, self.y)
