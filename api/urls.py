from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="РАССЫЛКИ API",
      default_version='v1',
      description="Тестовое задание",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="ezra.wick@ya.ru"),
      license=openapi.License(name="Ezra Wick"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

app_name = 'api'

urlpatterns = [
   path('client/all_clients/', views.ClientsAPI.as_view()),
   path('client/create/', views.ClientCreateAPI.as_view()),
   path('client/update/<int:pk>/', views.ClientUpdateAPI.as_view()),
   path('client/delete/<int:pk>/', views.ClientDeleteAPI.as_view()),

   path('mailing/', views.MailingListAPI.as_view()),
   path('mailing/statistics/', views.MailingInfoAPI.as_view()),
   path('mailing/create/', views.MailingCreateAPI.as_view()),
   path('mailing/retrieve/<int:pk>/', views.MailingAPI.as_view()),
   path('mailing/update/<str:job_id>/', views.MailingUpdateAPI.as_view()),
   path('mailing/delete/<int:pk>/', views.MailingDeleteAPI.as_view()),
   path('mailing/pause/<int:pk>/', views.MailingPauseAPI.as_view()),
   path('mailing/resume/<int:pk>/', views.MailingResumeAPI.as_view()),

   path('message/all_messages/', views.MessageAPI.as_view()),
   path('message/send/', views.SendMessageAPI.as_view()),

   path(
       'docs/',
       schema_view.with_ui('swagger', cache_timeout=0),
       name='schema-swagger-ui'
       ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
