from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # Reports CRUD + list/search
    path('reports/', views.report_list, name='report_list'),
    path('reports/create/', views.report_create, name='report_create'),
    path('reports/<int:pk>/', views.report_detail, name='report_detail'),
    path('reports/<int:pk>/edit/', views.report_update, name='report_update'),
    path('reports/<int:pk>/delete/', views.report_delete, name='report_delete'),
    path('reports/<int:pk>/resolve/', views.report_resolve, name='report_resolve'),

    # Own reports
    path('my-reports/', views.my_reports, name='my_reports'),
]


## Step 12 — Write `reports/urls.py` (new file)

# Create this file inside `reports/`:

"""

What's going on:
----------------
- `path('reports/<int:pk>/edit/', views.report_update, name='report_update')` — `<int:pk>` is a **URL converter**: it captures a number from the address (e.g. `5` from `/reports/5/edit/`) and passes it into the view as the `pk` keyword argument.

- `.as_view()` — class-based views (like `CustomLoginView`) need this conversion to become a plain function Django's router can call; regular function-based views (`views.home`) don't.

- `name='...'` — gives each URL a permanent nickname. Templates and views reference URLs by this name (`{% url 'report_detail' report.pk %}`, `redirect('report_detail', pk=report.pk)`) instead of hardcoding the path string — so if you ever change a path, nothing breaks elsewhere.


"""
