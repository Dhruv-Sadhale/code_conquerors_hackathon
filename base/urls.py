from django.urls import path
from . import views
from .views import home, submit_notification


urlpatterns = [
    # path('login/', views.loginPage, name="login"),
    path('logout/', views.logout_view, name="logout"),
    # path('register/', views.registerPage, name="register"),
    path('home/',views.home, name="home" ),

    path('',views.home, name="home" ),
   path('submit-notification/', submit_notification, name='submit_notification'),
    path('clubs/explore/<str:pk>/',views.explore,name='explore'),

    path('questionnaire/', views.gemini_response, name='questionnaire'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('satisfaction/', views.satisfaction, name='satisfaction'),
    path('generate_qrcode/<str:club_name>/', views.generate_qrcode, name='generate_qrcode'),
    path('attend_club/<str:club_name>/', views.attend_club, name='attend_club'),
    path('api/record_response/', views.record_response, name='record_response'),
    path('api/record_club/', views.record_club, name='record_club'),
    path('clubs/', views.clubs, name='clubs'),
    path('display_recommendations/', views.induction, name='display_recommendations'),
    path('core/<str:pk>/',views.core, name='core'),
    path('record_applicant/', views.record_applicant, name='record_applicant'),
    path('transfer_applicants/<str:club_name>/', views.transfer_applicants, name='transfer_applicants'),
    path( 'delete_user_response/', views.delete_user_response, name='delete_user_response'),
    path('email/', views.send_email, name='send_email'),
    path('gemini/', views.gemini_response, name='gemini_response'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    ]

