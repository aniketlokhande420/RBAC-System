from django.urls import path
from .views import UserView, PermissionView,  RoleManagementView, AccessValidationView, AccessLogView

urlpatterns = [
    path('users/', UserView.as_view(), name='user'),
    path('permissions/', PermissionView.as_view(), name='permission'),
    path('roles/', RoleManagementView.as_view(), name='role_management'),
    path('access-validation/', AccessValidationView.as_view(), name='access_validation'),
    path('logs/', AccessLogView.as_view(), name='logs'),
]
