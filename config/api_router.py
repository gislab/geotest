from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from coordmanager.api.views import UserRequestJobViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("userjob", UserRequestJobViewSet, basename='job')

app_name = "api"
urlpatterns = router.urls
