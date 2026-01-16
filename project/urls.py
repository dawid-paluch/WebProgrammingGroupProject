"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.http import HttpResponse
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from api import views as api_views



urlpatterns = [
    #login vs spa
    path("", api_views.root_view, name="root"),

    #auth
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=AuthenticationForm, redirect_authenticated_user=True), name='login'),
    path('signup/', api_views.signup, name='signup'),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    #api
    path('api/', include('api.urls')),

    #health & admin
    path('health', lambda request: HttpResponse("OK")),
    path('admin/', admin.site.urls),

    path(
        "app/",
        login_required(
            ensure_csrf_cookie(
                TemplateView.as_view(template_name="api/spa/index.html")
            )
        ),
        name="spa",
    ),

    #SPA entry point
    re_path(
        r"^(?!login/|signup/|logout/|api/|admin/).*$",
        login_required(
            ensure_csrf_cookie(
                TemplateView.as_view(template_name="api/spa/index.html")
            )
        ),
    ),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
