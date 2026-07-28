from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        # درخواست‌های فقط خواندنی
        if request.method in SAFE_METHODS:
            return True

        # فقط ادمین بتواند تغییر دهد
        return request.user and request.user.is_staff