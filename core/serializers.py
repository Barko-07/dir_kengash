from rest_framework import serializers
from .models import User, Region, PedagogicalCenter, Course, CourseEnrollment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class PedagogicalCenterSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.name', read_only=True)
    director_name = serializers.CharField(source='director.username', read_only=True)
    
    class Meta:
        model = PedagogicalCenter
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )
    
    class Meta:
        model = CourseEnrollment
        fields = ['id', 'user', 'course', 'course_id', 'enrolled_at', 'completed']
        read_only_fields = ['user', 'completed']


