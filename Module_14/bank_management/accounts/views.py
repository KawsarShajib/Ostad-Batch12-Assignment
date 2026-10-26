from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User

from .models import BankAccount
from .permissions import IsOwnerOrAdmin
# from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserRegistrationSerializer, 
    UserProfileSerializer,
    BankAccountSerializer,
    BankAccountDetailSerializer,
    BalanceSerializer,
)


""" 

    Order follows the customer journey: 
        register → login → profile → accounts → balance → admin 

"""

class IsOwnerOrAdmin(permissions.BasePermission):
    """Custom permission: only owner or admin can access."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.owner == request.user
    

# ---------- Authentication ----------
class RegisterView(generics.CreateAPIView):
    """
    Register a new customer.
    Anyone can access this endpoint (no authentication required).
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create authentication token for the new user
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Registration successful.",
            "token": token.key,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }, status=status.HTTP_201_CREATED)



class LoginView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'message': 'Login successful.',
        })


# ---------- Profile ----------
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ---------- Bank accounts (customer) ----------
class AccountListCreateView(generics.ListCreateAPIView):
    """List own accounts or create a new account."""
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:                      # admin sees everything
            return BankAccount.objects.all()
        return BankAccount.objects.filter(owner=user)
    
    def perform_create(self, serializer):
        # owner comes from the token, not from the request body
        serializer.save(owner=self.request.user)


class AccountDetailView(generics.RetrieveAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return BankAccount.objects.all()
        return BankAccount.objects.filter(owner=user)


class AccountBalanceView(generics.RetrieveAPIView):
    serializer_class = BalanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = 'id'

    def get_queryset(self):
        if self.request.user.is_staff:
            return BankAccount.objects.all()
        return BankAccount.objects.filter(owner=self.request.user)


# ---------- Admin only ----------
class AdminCustomerListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminAccountListView(generics.ListAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountDetailSerializer
    permission_classes = [permissions.IsAdminUser]