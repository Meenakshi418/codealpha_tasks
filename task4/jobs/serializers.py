from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Candidate, Employer, Job,Application, Resume, Notification


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=["candidate", "employer"])

    phone = serializers.CharField(required=False)
    skills = serializers.CharField(required=False)
    company_name = serializers.CharField(required=False)
    company_description = serializers.CharField(required=False)

    def create(self, validated_data):
        role = validated_data.pop("role")

        phone = validated_data.pop("phone", "")
        skills = validated_data.pop("skills", "")
        company_name = validated_data.pop("company_name", "")
        company_description = validated_data.pop(
            "company_description", ""
        )

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        if role == "candidate":
            Candidate.objects.create(
                user=user,
                phone=phone,
                skills=skills
            )

        elif role == "employer":
            Employer.objects.create(
                user=user,
                company_name=company_name,
                company_description=company_description
            )

        return user

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "location",
            "salary",
            "created_at"
        ]
        read_only_fields = ["id", "created_at"]

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            "id",
            "job",
            "candidate",
            "status",
            "applied_at"
        ]
        read_only_fields = [
            "id",
            "candidate",
            "status",
            "applied_at"
        ]


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            "id",
            "resume_file",
            "uploaded_at"
        ]
        read_only_fields = [
            "id",
            "uploaded_at"
        ]

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = [
            "id",
            "message",
            "is_read",
            "created_at"
        ]

        read_only_fields = [
            "id",
            "message",
            "created_at"
        ]   