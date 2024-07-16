from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from rest_framework import serializers
from .models import HHMSUser, Session
from .connection import execute_raw_sql
import uuid
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = HHMSUser
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'contact_number','date_of_birth', 'type', 'latitude', 'longitude', 'address']
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['is_active'] = True
        validated_data['is_staff'] = False
        validated_data['is_superuser'] = False
        validated_data['date_joined'] = timezone.now()
        
        insert_query = """
        INSERT INTO authUser_hhmsuser (username, password, email, first_name, last_name, is_active, date_joined, contact_number, type, is_staff, is_superuser, latitude, longitude, address, date_of_birth  )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        params = [
            validated_data['username'],
            validated_data['password'],
            validated_data['email'],
            validated_data['first_name'],
            validated_data['last_name'],
            validated_data['is_active'],
            validated_data['date_joined'],
            validated_data['contact_number'],
            validated_data['type'],
            validated_data['is_staff'],
            validated_data['is_superuser'],
            validated_data['latitude'],
            validated_data['longitude'],
            validated_data['address'],
            validated_data['date_of_birth']
        ]
        
        
        execute_raw_sql(insert_query, params)
        
        
        select_query = """
        SELECT * 
        FROM authUser_hhmsuser
        WHERE username = %s;
        """
        result = execute_raw_sql(select_query, [validated_data['username']])
        
        return result[0] if result else None


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        select_query = """
        SELECT * 
        FROM authUser_hhmsuser
        WHERE email = %s;
        """
        result = execute_raw_sql(select_query, [email])
        
        if not result:
            raise serializers.ValidationError("Invalid email or password")
        
        user = result[0]
        
        if not check_password(password, user['password']):
            raise serializers.ValidationError("Invalid email or password")
        
        data['user'] = user
        return data
    
    def create_session(self, user):
        session_token = str(uuid.uuid4())
        
        delete_query = """
        DELETE FROM authUser_session WHERE user_id = %s;
        """
        execute_raw_sql(delete_query, [user['id']])
        
        insert_query = """
        INSERT INTO authUser_session (user_id, session_token, created_at)
        VALUES (%s, %s, %s);
        """
        params = [user['id'], session_token, timezone.now()]
        
        execute_raw_sql(insert_query, params)
        
        return session_token

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = HHMSUser
        fields = ['type', 'first_name', 'last_name', 'id']