import logging
from django.db import transaction
from coordmanager.models import UserRequestJob
from coordmanager.tasks import evaluate_result
from rest_framework import serializers

logger = logging.getLogger(__name__)

class UserRequestJobSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        """
        Create and return a new `UserRequestJob`
        instance and calculate the result asyncron.
        """
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        logger.info('receive request job from user %s', user)
        instance = UserRequestJob.objects.create(**validated_data, user=user)
        logger.info('create job id: %s', instance.id)
        transaction.on_commit(lambda: evaluate_result.delay(instance.id))
        return instance

    class Meta:
        model = UserRequestJob
        fields = ["id", "status", "user_id", "x", "y",
                  "operation", "num_point", "results"]
