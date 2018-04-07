from employee.models import EmployeePermission
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class employee_permission(object):

    def __init__(self, permission):
        self.permission = permission

    def __call__(self, f):
        def wrapped_f(*args, file_id=None, emp_id=None, permission_id=None):
            request = args[0]

            if EmployeePermission.has_perm(request.user, self.permission):
                if file_id:
                    return f(*args, file_id)

                elif emp_id:
                    return f(*args, emp_id)

                elif permission_id:
                    return f(*args, permission_id)
                else:
                    return f(*args)

            else:
                return HttpResponseRedirect(reverse('employee:access_denied'))

        return wrapped_f
