from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('users/', views.users),
    path('users/<int:id>/', views.user),
    path('users/users/', views.get_only_users),
    path('users/admins/', views.get_only_admins),
    path('users/archived/<str:type>/', views.get_archived_users),
    path('users/password/reset/<int:id>/', views.change_password),
    path('cases/', views.cases),
    path('cases/user/<int:id>/', views.get_user_cases),
    path('cases/queue/', views.get_unassigned_cases),
    path('cases/archived/', views.get_archived_cases),
    path('cases/assign/', views.assign_admin_to_case),
    path('cases/<int:id>/', views.case),
    path('updates/', views.updates),
    path('updates/<int:id>/', views.update),
]
