from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views import View
from .models import User, Permission, RolePermission, AccessLog
import json

@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):

    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        if role not in [role[0] for role in User.ROLES]:
            return JsonResponse({"success": False, "message": "Invalid role"}, status=400)
        try:
            user = User.objects.create_user(username=username, password=password, role=role)
        except Exception as e:
            return JsonResponse({"success": False, "message": "Unable to create User."}, status=500)
        return JsonResponse({"success": True, "message": "User created successfully", "data": {"id": user.id, "username": user.username, "role": user.role}})

    def get(self, request):
        users = User.objects.all().values('id', 'username', 'role')
        return JsonResponse({"success": True, "data": list(users)})

@method_decorator(csrf_exempt, name='dispatch')
class PermissionView(View):

    def post(self, request):
        """Only supervisors and admin users can access this API."""
        data = json.loads(request.body)
        username = data.get('username')
        permission_name = data.get('permission_name')
        resource = data.get('resource')
        action = data.get('action')
        username = data.get('username')

        if not username or not permission_name or not resource or not action:
            return JsonResponse({"success": False, "message": "Missing required fields"}, status=400)

        # if request.user.role not in ['supervisor', 'admin']:
        try:
            user_role = User.objects.get(username=username).role
        except:
            return JsonResponse({"success": False, "message": "User does not exist."}, status=404)
        # print("user_role: ",user_role)
        if user_role not in ['supervisor', 'admin']:

            return JsonResponse({"success": False, "message": "Only supervisors and admins can define permissions."}, status=403)

        permission, created = Permission.objects.get_or_create(name=permission_name, resource=resource, action=action)
        if created:
            return JsonResponse({"success": True, "message": "Permission created successfully."})

        return JsonResponse({"success": False, "message": "Permission already exists."})

    def get(self, request):
        permissions = Permission.objects.values('name', 'resource', 'action')
        return JsonResponse({"success": True, "data": list(permissions)})

@method_decorator(csrf_exempt, name='dispatch')
class RoleManagementView(View):

    def post(self, request):
        """Only admin users can access this API"""
        data = json.loads(request.body)
        username = data.get('username')
        role = data.get('role_to_assign_permission')
        permission_name = data.get('permission_name')
        
        if not username or not role or not permission_name:
            return JsonResponse({"success": False, "message": "Missing required fields"}, status=400)
        try:
            user_role = User.objects.get(username=username).role
        except:
            return JsonResponse({"success": False, "message": "User does not exist."}, status=404)
        print("user_role: ",user_role)
        if user_role != 'admin':
            return JsonResponse({"success": False, "message": "Only admins can assign permissions to roles."}, status=403)

        permission = Permission.objects.filter(name=permission_name).first()
        if not permission:
            return JsonResponse({"success": False, "message": "Permission does not exist."}, status=404)

        RolePermission.objects.create(role=role, permission=permission)
        return JsonResponse({"success": True, "message": "Permission assigned to role successfully."})

    def get(self, request):
        role_permissions = []
        for role in User.ROLES:
            role_permissions.append(list(RolePermission.objects.filter(role=role[0]).values()))
        return JsonResponse({"success": True, "data": role_permissions})

@method_decorator(csrf_exempt, name='dispatch')
class AccessValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        action = data.get('action')
        resource = data.get('resource')

        if not username or not action or not resource:
            return JsonResponse({"success": False, "message": "Missing required fields"}, status=400)
        user = User.objects.filter(username=username).first()
        if not user:
            return JsonResponse({"success": False, "message": "User not found"}, status=404)

        role_permissions = RolePermission.objects.select_related('permission').filter(role=user.role, permission__resource=resource, permission__action=action)

        print("role permission: ",RolePermission.objects.filter(role=user.role).values())
        outcome = role_permissions.exists()

        AccessLog.objects.create(user=user, action=action, resource=resource, outcome=outcome)

        if outcome:
            return JsonResponse({"success": True, "message": "Access granted"})
        else:
            return JsonResponse({"success": False, "message": "Access denied"}, status=403)


@method_decorator(csrf_exempt, name='dispatch')
class AccessLogView(View):

    def get(self, request):
        try:
            hours = int(request.GET.get('hours', 24))  # Default to past 24 hours
            if hours <= 0:
                return JsonResponse({"success": False, "message": "Hours parameter must be positive."}, status=403)
        except ValueError:
            return JsonResponse({"success": False, "message": "Invalid hours parameter."}, status=400)

        from django.utils.timezone import now, timedelta
        start_time = now() - timedelta(hours=hours)

        logs = AccessLog.objects.filter(timestamp__gte=start_time).values('user__username', 'action', 'resource', 'outcome', 'timestamp')
        return JsonResponse({"success": True, "data": list(logs)})
