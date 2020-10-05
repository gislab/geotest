from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CoordinateManager


class Coordinate(models.Model):
    """
    Stores coordinates points
    """
    x = models.FloatField(help_text=_("longitude"))
    y = models.FloatField(help_text=_("latitude"))
    objects = CoordinateManager()

    class Meta:
        verbose_name = _("coordinate")
        verbose_name_plural = _("coordinates")

    def __str__(self):
        return 'coordinate(id=%s, x=%s, y=%s)' % (self.id, self.x, self.y)


class UserRequestJob(models.Model):
    """
    Calculate and Store the nearest or farthest
    points to user submitted coordinates
    """
    NEAREST = 'N'
    FURTHEST = 'F'
    OPERATION_CHOICES = (
        (NEAREST, _("nearest point")),
        (FURTHEST, _("furthest point")),
    )

    EVALUATED = 'evaluated'
    PENDING = 'pending'

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    x = models.FloatField(help_text=_("longitude"))
    y = models.FloatField(help_text=_("latitude"))
    operation = models.CharField(
        max_length=1,
        choices=OPERATION_CHOICES,
        help_text=_('operation type'),
        blank=False
    )
    num_point = models.PositiveIntegerField(help_text=_('number of points to be returned'))
    request_datetime = models.DateTimeField(
        help_text=_('request date time'),
        editable=False,
        auto_now_add=True
    )
    evaluation_datetime = models.DateTimeField(
        help_text=_('result evaluation date time'),
        null=True,
        default=None,
        editable=False
    )
    results = ArrayField(
        ArrayField(
            models.FloatField(),
            size=2,
        ),
        null=True,
        default=None,
        editable=False
    )

    class Meta:
        verbose_name = _("result")
        verbose_name_plural = _("results")
        ordering = ['-request_datetime',]

    @property
    def status(self):
        return self.EVALUATED if self.evaluation_datetime is not None else self.PENDING

    def get_results(self):
        qs = Coordinate.objects.distance(self.x, self.y)
        if self.operation == self.NEAREST:
            qs = qs.order_by('distance')
        else:
            qs = qs.order_by('-distance')

        results = []
        for coordinate in qs[0:self.num_point]:
            results.append((coordinate.x, coordinate.y))
        return results

    def evaluate_result(self, commit=False):
        self.evaluation_datetime = timezone.now()
        self.results = self.get_results()
        if commit is True:
            self.save()

    def __str__(self):
        return 'coordinate(id=%s, user_id=%s, request_date=%s, status=%s)' % (
            self.id, self.user_id, self.request_datetime, self.status)
