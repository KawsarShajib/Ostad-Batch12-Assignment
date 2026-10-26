from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import BankAccount

# 1) Registration (used by RegisterView)
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user

# 2) Profile (used by ProfileView and AdminCustomerListView)
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'username', 'date_joined')

# 3) Bank account: create and list for customers
# Purpose: Convert models <--> JSON and perform validation.
class BankAccountSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = BankAccount
        fields = (
            'id', 
            'account_number', 
            'account_type', 
            'balance',
            'owner', 
            'owner_username', 
            'status', 
            'created_at', 
            'updated_at'
        )

        # customers shouldn’t be able to set their own following credentials : 
        read_only_fields = (
            'id', 
            'account_number', 
            'balance', 
            'owner', 
            'status',
            'created_at', 
            'updated_at'
        )

    def create(self, validated_data):
        # Owner will be set from the logged-in user later
        # For now we can accept owner in the request body (temporary)    
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


# 4) Bank account: full read-only detail for admin
class BankAccountDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    owner_email = serializers.CharField(source='owner.email', read_only=True)

    class Meta:
        model = BankAccount
        fields = ('id', 'account_number', 'account_type', 'balance',
                  'owner', 'owner_username', 'owner_email', 'status',
                  'created_at', 'updated_at')
        read_only_fields = fields


# 5) Balance check
class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ('account_number', 'balance', 'account_type', 'status')


