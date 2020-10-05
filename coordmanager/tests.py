import base64
import datetime
import pytz
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest import mock
from coordmanager.models import UserRequestJob
from coordmanager.api.serializers import UserRequestJobSerializer


def get_client(user=None):
    client = APIClient()
    if user:
        client.force_authenticate(user=user)
    return client


class UserRequestJobApiTest(TestCase):

    def setUp(self):
        self.url = reverse('api:job-list')
        self.user1 = User.objects.create_user(username='test_user1', password='user1', email='test1@test.it', id=2)
        self.user2 = User.objects.create_user(username='test_user2', password='user2', email='test2@test.it', id=3)
        UserRequestJob.objects.create(x='100', y='100', operation=UserRequestJob.NEAREST, num_point=2, user=self.user1)
        UserRequestJob.objects.create(x='200', y='200', operation=UserRequestJob.NEAREST, num_point=2, user=self.user1)
        UserRequestJob.objects.create(x='300', y='300', operation=UserRequestJob.NEAREST, num_point=2, user=self.user2)
        UserRequestJob.objects.create(x='400', y='400', operation=UserRequestJob.NEAREST, num_point=2, user=self.user2)

    def test_user_request_job_serializer(self):
        job = UserRequestJob.objects.all()[0]
        job_json = {
            'id': job.id,
            'status': job.status,
            'user_id': job.user_id,
            'x': job.x,
            'y': job.y,
            'operation': job.operation,
            'num_point': job.num_point,
            'results': job.results
        }
        serializer = UserRequestJobSerializer(job, many=False)
        self.assertEqual(job_json, serializer.data)

    def test_unauthorized_request(self):
        client = get_client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_basic_autentication(self):
        client = get_client()
        auth_headers = {
            'HTTP_AUTHORIZATION': b'Basic ' + base64.b64encode(b'test_user1:user1'),
        }
        response = client.get(self.url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_request_job_bad_request(self):
        client = get_client(self.user1)
        response = client.post(self.url, {
            'x' : 300,
            'y': 100,
            'num_point' : 3
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_request_job_list(self):
        def test_user_list(user):
            client = get_client(user)
            response = client.get(self.url)
            jobs = UserRequestJob.objects.filter(user=user).order_by('-request_datetime')
            serializer = UserRequestJobSerializer(jobs, many=True)
            self.assertEqual(response.data, serializer.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_user_list(self.user1)
        test_user_list(self.user2)

    def test_user_request_job_create(self):
        num = UserRequestJob.objects.filter(user=self.user1).count()
        mocked = datetime.datetime(2020, 4, 4, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            client = get_client(self.user1)
            response = client.post(self.url, {
                'x' : 300,
                'y': 100,
                'operation': UserRequestJob.NEAREST,
                'num_point' : 3
            })
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            num1 = UserRequestJob.objects.filter(user=self.user1).count()
            self.assertEqual(num + 1, num1)
            job = UserRequestJob.objects.get(id=response.data['id'])
            serializer = UserRequestJobSerializer(job, many=False)
            self.assertEqual(response.data, serializer.data)
            self.assertEqual(job.request_datetime, mocked)
            self.assertEqual(job.x, 300)
            self.assertEqual(job.y, 100)
            self.assertEqual(job.num_point, 3)
            self.assertEqual(job.user, self.user1)
            self.assertEqual(job.operation, UserRequestJob.NEAREST)
            self.assertEqual(job.results, None)
            self.assertEqual(job.evaluation_datetime, None)
            self.assertEqual(job.status, UserRequestJob.PENDING)
