from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User
from apps.curriculum.models import Subject


class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(read_only=True)
    is_instructor = serializers.BooleanField(read_only=True)
    is_student = serializers.BooleanField(read_only=True)
    display_name = serializers.CharField(read_only=True)
    assigned_subject_name = serializers.CharField(source='assigned_subject.name', read_only=True)
    assigned_subject_slug = serializers.CharField(source='assigned_subject.slug', read_only=True)
    assigned_batches_list = serializers.SerializerMethodField()
    enrolled_batches_list = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'display_name',
            'role', 'mobile_number', 'pin_code', 'assigned_subject',
            'assigned_subject_name', 'assigned_subject_slug', 'is_admin',
            'is_instructor', 'is_student', 'is_admin_role', 'batch_name',
            'avatar_url', 'bio', 'is_active', 'is_active_account', 'date_joined',
            'assigned_batches_list', 'enrolled_batches_list'
        ]
        read_only_fields = ['id', 'date_joined', 'is_admin', 'is_instructor', 'is_student', 'display_name']

    def get_assigned_batches_list(self, obj):
        if hasattr(obj, 'assigned_batches'):
            return [{'id': b.id, 'name': b.name, 'course_name': b.course.name} for b in obj.assigned_batches.all()]
        return []

    def get_enrolled_batches_list(self, obj):
        if hasattr(obj, 'enrolled_batches'):
            return [{'id': b.id, 'name': b.name, 'course_name': b.course.name, 'schedule': b.schedule} for b in obj.enrolled_batches.all()]
        return []


class AdminUserManageSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True, min_length=4)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'role',
            'mobile_number', 'pin_code', 'assigned_subject', 'is_admin_role',
            'batch_name', 'avatar_url', 'bio', 'is_active', 'is_active_account', 'password'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None) or validated_data.get('pin_code') or 'kalari123'
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class StudentRegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150, required=True)
    mobile_number = serializers.CharField(max_length=20, required=True)
    email = serializers.EmailField(required=True)
    pin = serializers.CharField(min_length=4, max_length=8, required=True)
    batch_name = serializers.CharField(max_length=100, required=False, default="Batch 2026")

    def validate_mobile_number(self, value):
        cleaned = value.strip().replace(" ", "").replace("-", "")
        if User.objects.filter(mobile_number=cleaned).exists() or User.objects.filter(username=cleaned).exists():
            raise serializers.ValidationError("A student with this mobile number is already registered.")
        return cleaned

    def validate_email(self, value):
        cleaned = value.strip().lower()
        if User.objects.filter(email__iexact=cleaned).exists():
            raise serializers.ValidationError("A student with this email address is already registered.")
        return cleaned

    def validate_pin(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("PIN must contain only numbers (e.g. 1234).")
        return value

    def create(self, validated_data):
        mobile = validated_data['mobile_number']
        user = User(
            username=mobile,
            first_name=validated_data['name'],
            email=validated_data['email'],
            mobile_number=mobile,
            pin_code=validated_data['pin'],
            role='STUDENT',
            batch_name=validated_data.get('batch_name', 'Batch 2026')
        )
        user.set_password(validated_data['pin'])
        user.save()
        return user


class StaffUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    assigned_subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source='assigned_subject',
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'first_name',
            'last_name', 'assigned_subject', 'assigned_subject_id', 'is_admin_role', 'mobile_number', 'bio'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['role'] = 'STAFF'
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    identifier = serializers.CharField(required=False, write_only=True)
    secret = serializers.CharField(required=False, write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['password'].required = False

    def validate(self, attrs):
        identifier = attrs.get('identifier') or attrs.get('username')
        secret = attrs.get('secret') or attrs.get('password')

        if not identifier or not secret:
            raise serializers.ValidationError("Both login identifier (mobile/email/username) and PIN/password are required.")

        identifier = identifier.strip()

        # Lookup user by mobile, email, or username
        user = (
            User.objects.filter(mobile_number=identifier).first() or
            User.objects.filter(email__iexact=identifier).first() or
            User.objects.filter(username__iexact=identifier).first()
        )

        if not user:
            raise serializers.ValidationError("No account found with this mobile number, email, or username.")

        # Verify password or PIN
        if not user.check_password(secret) and user.pin_code != secret:
            raise serializers.ValidationError("Incorrect PIN or password. Please verify and try again.")

        if not user.is_active or not getattr(user, 'is_active_account', True):
            raise serializers.ValidationError("This account has been deactivated.")

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role', 'batch_name', 'mobile_number']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
