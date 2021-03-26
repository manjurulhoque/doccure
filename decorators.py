from django.core.exceptions import PermissionDenied


def user_is_doctor(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == "doctor":
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap
