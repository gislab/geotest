from django.db import models
from django.db.models.functions import Sqrt, Power


class CoordinateManager(models.Manager):

    def distance(self, x, y):
        """ calculate euclidean distance as annotation """
        return self.annotate(
            distance=Sqrt(
                Power(models.F('x') - x, 2) +
                Power(models.F('y') - y, 2)
            )
        )
