from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/dashboard-data/", views.dashboard_data, name="dashboard_data"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("add_lead/", views.add_lead, name="add_lead"),
    path("lead/", views.lead, name="lead"),
    path('deal', views.deals_dashboard, name='deals_dashboard'),
    path('tasks/', views.tasks_dashboard, name='tasks_dashboard'),
    
    # APIs 
    path('lead/<int:lead_id>/', views.lead_detail, name='lead_detail'),
    path('lead/<int:lead_id>/convert/', views.convert_to_deal, name='convert_to_deal'),
    path('delete-lead/<int:lead_id>/', views.delete_lead, name='delete_lead'),
    path('activity/delete/<int:activity_id>/', views.delete_activity, name='delete_activity'),
    path('delete-multiple-leads/', views.delete_multiple_leads, name='delete_multiple_leads'),
    path('deal/<int:deal_id>/', views.deal_profile, name='deal_profile'),
    path('deal/<int:deal_id>/delete/', views.delete_deal, name='delete_deal'),
    path('deal/<int:deal_id>/status/<str:status_choice>/', views.update_deal_status, name='update_deal_status'),
    path('deal/<int:deal_id>/add-task/', views.add_task, name='add_task'),
    path('deal/<int:deal_id>/tasks/', views.task_profile, name='task_profile'),
    path('task/<int:task_id>/toggle/', views.toggle_task_status, name='toggle_task_status'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),




    
]