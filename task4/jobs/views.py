from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Employer, Job, Candidate, Application, Resume, Notification
from .serializers import (
    RegisterSerializer,
    JobSerializer,
    ApplicationSerializer,
    ResumeSerializer,
    NotificationSerializer
)


# REGISTER
@api_view(["POST"])
def register(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            {"message": "Registration successful"},
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# LOGIN
@api_view(["POST"])
def login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(
        username=username,
        password=password
    )

    if user is None:
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token, created = Token.objects.get_or_create(user=user)

    return Response({
        "message": "Login successful",
        "token": token.key
    })


# JOB LIST + SEARCH + CREATE
@api_view(["GET", "POST"])
def jobs_api(request):

    # GET JOBS
    if request.method == "GET":

        jobs = Job.objects.all().order_by("-created_at")

        search = request.GET.get("search")
        location = request.GET.get("location")
        salary_min = request.GET.get("salary_min")
        salary_max = request.GET.get("salary_max")

        if search:
            jobs = jobs.filter(title__icontains=search)

        if location:
            jobs = jobs.filter(location__icontains=location)

        if salary_min:
            jobs = jobs.filter(salary__gte=salary_min)

        if salary_max:
            jobs = jobs.filter(salary__lte=salary_max)

        serializer = JobSerializer(jobs, many=True)

        return Response(serializer.data)

    # CREATE JOB
    if request.method == "POST":

        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            employer = request.user.employer
        except Employer.DoesNotExist:
            return Response(
                {"error": "Only employers can post jobs."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(employer=employer)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# APPLY FOR JOB
@api_view(["POST"])
def apply_job(request, job_id):

    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        candidate = request.user.candidate
    except Candidate.DoesNotExist:
        return Response(
            {"error": "Only candidates can apply for jobs."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response(
            {"error": "Job not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    if Application.objects.filter(
        job=job,
        candidate=candidate
    ).exists():

        return Response(
            {"error": "You have already applied for this job."},
            status=status.HTTP_400_BAD_REQUEST
        )

    application = Application.objects.create(
        job=job,
        candidate=candidate
    )
    Notification.objects.create(
        user=job.employer.user,
        message=f"{candidate.user.username} applied for your job: {job.title}"
    )

    serializer = ApplicationSerializer(application)

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


# CANDIDATE APPLICATIONS
@api_view(["GET"])
def my_applications(request):

    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        candidate = request.user.candidate
    except Candidate.DoesNotExist:
        return Response(
            {"error": "Only candidates can view applications."},
            status=status.HTTP_403_FORBIDDEN
        )

    applications = Application.objects.filter(
        candidate=candidate
    ).order_by("-applied_at")

    serializer = ApplicationSerializer(
        applications,
        many=True
    )

    return Response(serializer.data)


# RESUME UPLOAD
@api_view(["POST"])
def upload_resume(request):

    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        candidate = request.user.candidate
    except Candidate.DoesNotExist:
        return Response(
            {"error": "Only candidates can upload resumes."},
            status=status.HTTP_403_FORBIDDEN
        )

    resume_file = request.FILES.get("resume_file")

    if not resume_file:
        return Response(
            {"error": "Resume file is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    resume, created = Resume.objects.update_or_create(
        candidate=candidate,
        defaults={
            "resume_file": resume_file
        }
    )

    serializer = ResumeSerializer(resume)

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
    )


# EMPLOYER APPLICATIONS
@api_view(["GET"])
def employer_applications(request):

    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        employer = request.user.employer
    except Employer.DoesNotExist:
        return Response(
            {"error": "Only employers can view applications."},
            status=status.HTTP_403_FORBIDDEN
        )

    applications = Application.objects.filter(
        job__employer=employer
    ).order_by("-applied_at")

    serializer = ApplicationSerializer(
        applications,
        many=True
    )

    return Response(serializer.data)


# UPDATE APPLICATION STATUS
@api_view(["PATCH"])
def update_application_status(request, application_id):

    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        employer = request.user.employer
    except Employer.DoesNotExist:
        return Response(
            {"error": "Only employers can update applications."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        application = Application.objects.get(
            id=application_id,
            job__employer=employer
        )
    except Application.DoesNotExist:
        return Response(
            {"error": "Application not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    new_status = request.data.get("status")

    valid_statuses = [
        "APPLIED",
        "SHORTLISTED",
        "REJECTED",
        "SELECTED"
    ]

    if new_status not in valid_statuses:
        return Response(
            {
                "error": "Invalid status.",
                "allowed": valid_statuses
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    application.status = new_status
    application.save()

    Notification.objects.create(
        user=application.candidate.user,
        message=(
            f"Your application for '{application.job.title}' "
            f"has been updated to {new_status}."
        )
    )

    serializer = ApplicationSerializer(application)

    return Response(serializer.data)

@api_view(["GET"])
def notifications(request):

    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    user_notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    serializer = NotificationSerializer(
        user_notifications,
        many=True
    )

    return Response(serializer.data)