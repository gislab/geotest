import logging
from config import celery_app
from coordmanager.models import UserRequestJob

logger = logging.getLogger(__name__)

@celery_app.task()
def evaluate_result(user_job_id):
    """
    calculate user job request task
    """
    logger.info("evaluate user job id=%s", user_job_id)
    user_job = UserRequestJob.objects.get(id=user_job_id)
    user_job.evaluate_result(commit=True)
