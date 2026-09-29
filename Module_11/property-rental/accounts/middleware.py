from django.contrib import messages
from django.shortcuts import redirect


class RoleBasedAccessMiddleware:
    """
    Custom middleware that enforces role-based access at the request level,
    on top of view-level permission checks (defence in depth).

    - Only Property Owners may reach owner-only paths (add/edit/delete
      properties, manage rental requests received on their properties).
    - Only Tenants may reach tenant-only paths (sending a rental request,
      viewing "my requests", leaving reviews).
    - Anonymous users are simply passed through to Django's normal
      @login_required handling on the view, so they still get redirected
      to the login page rather than a generic permission error here.
    """

    OWNER_ONLY_PREFIXES = (
        '/properties/create/',
        '/properties/edit/',
        '/properties/delete/',
        # addition of image gallery for a property
        '/properties/image/delete/',
        '/rentals/owner/',
    )

    TENANT_ONLY_PREFIXES = (
        '/rentals/request/',
        '/rentals/my-requests/',
        '/rentals/cancel/',
        '/rentals/review/',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        path = request.path

        if user is not None and user.is_authenticated:
            if path.startswith(self.OWNER_ONLY_PREFIXES) and not user.is_owner:
                messages.error(request, "That area is only available to property owners.")
                return redirect('properties:list')

            if path.startswith(self.TENANT_ONLY_PREFIXES) and not user.is_tenant:
                messages.error(request, "That area is only available to tenants.")
                return redirect('properties:list')

        return self.get_response(request)
