"""
URL configuration for jobboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from jobs.views import (
    register,
    login,
    jobs_api,
    apply_job,
    my_applications,
    upload_resume,
    employer_applications,
    update_application_status,
    notifications
)


urlpatterns = [

    path("admin/", admin.site.urls),

    # Authentication
    path("api/register/", register),
    path("api/login/", login),

    # Jobs
    path("api/jobs/", jobs_api),

    # Applications
    path(
        "api/jobs/<int:job_id>/apply/",
        apply_job
    ),

    path(
        "api/applications/my/",
        my_applications
    ),

    path(
        "api/applications/employer/",
        employer_applications
    ),

    path(
        "api/applications/<int:application_id>/status/",
        update_application_status
    ),

    # Resume
    path(
        "api/resume/",
        upload_resume
    ),

    path(
        "api/notifications/",
        notifications
    ),
]


urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)