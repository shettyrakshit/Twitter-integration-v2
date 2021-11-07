from django.urls import path
from .views import SocialConnectView

urlpatterns = [path('<str:version>/connect/<str:platform>/',
                    SocialConnectView.as_view(),
                    name='social-connect')]
