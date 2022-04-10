from rest_framework.permissions import BasePermission
from .models import Task
class IsStaffUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class Tasks():
    def fetch_tasks(self):
        return Task.objects.all()

    def fetch_task(self, id):
        return Task.objects.filter(id=id).first()