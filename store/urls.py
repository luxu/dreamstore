from django.urls import include, path
from rest_framework import routers

from . import views as v

router = routers.DefaultRouter()
router.register(r"store", v.ProductViewSet)

urlpatterns = [
    path("", include(router.urls), name="api"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
