from django.urls import path
from . import views

app_name = 'detector'

urlpatterns = [
    # Main Plant Disease Predictor
    path('', views.home_view, name='home'),

    # User Authentication Routes
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Informational & Profile Routes (Multi-Page App Structure)
    path('how-it-works/', views.how_it_works_view, name='how_it_works'),
    path('about/', views.about_view, name='about'),
    path('profile/', views.profile_view, name='profile'),

    # Authenticated User Dashboard & History Routes
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('history/', views.history_view, name='history'),
    path('history/<int:id>/', views.history_detail_view, name='history_detail'),
    path('history/<int:id>/delete/', views.delete_history_view, name='history_delete'),
    path('history/clear/', views.clear_history_view, name='history_clear'),
]

