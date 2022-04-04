from django.urls import path

from . import views

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
]
