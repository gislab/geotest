from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from coordmanager.api.serializers import UserRequestJobSerializer
from coordmanager.models import UserRequestJob


class UserRequestJobViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = UserRequestJobSerializer
    queryset = UserRequestJob.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user_id=self.request.user.id).order_by('-request_datetime')
