# Import the built-in Django User model because our API will create new users.
from django.contrib.auth.models import User

# Import tools from Django REST Framework (DRF) that make building APIs super easy.
# generics provides pre-built views for common tasks (like CreateAPIView for making a new object).
# viewsets provide full CRUD (Create, Read, Update, Delete) capabilities in one class.
from rest_framework import generics, viewsets

# Import permissions. 
# AllowAny means anyone on the internet can hit this URL. 
# IsAuthenticated means they MUST have a valid token to proceed.
from rest_framework.permissions import AllowAny, IsAuthenticated

# Import pagination. This prevents our API from crashing if a user has 1,000,000 transactions!
# It sends them in "pages" (e.g., 10 at a time).
from rest_framework.pagination import LimitOffsetPagination

# Import the serializers we built to translate our Models into JSON.
from .serializers import UserRegistrationSerializer, CategorySerializer, TransactionSerializer

# Import our actual database models.
from .models import Category, Transaction

# =====================================================================
# REGISTER VIEW
# This is a generic "Create" view because its ONLY job is to create a new user.
# =====================================================================
class RegisterView(generics.CreateAPIView):
    """
    API endpoint for registering a new user.
    Open to everyone (AllowAny) because you shouldn't need an account to make an account!
    """
    # Tell DRF which database table we are querying (the User table).
    queryset = User.objects.all()
    
    # We set permissions to AllowAny so unregistered guests can sign up.
    permission_classes = (AllowAny,)
    
    # Tell DRF to use our custom serializer to validate the username/password before saving.
    serializer_class = UserRegistrationSerializer


# =====================================================================
# CATEGORY VIEWSET
# A ViewSet automatically handles GET (list all), POST (create), 
# GET (retrieve one), PUT (update one), and DELETE (delete one).
# =====================================================================
class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to perform CRUD operations on their categories.
    Restricted to authenticated users only.
    """
    # Tell DRF how to turn Category objects into JSON.
    serializer_class = CategorySerializer
    
    # Security checkpoint: block anyone who isn't logged in with a valid JWT token.
    permission_classes = (IsAuthenticated,)

    # We override the default "get_queryset" method to enforce multi-tenancy isolation.
    # Instead of returning ALL categories in the database, we ONLY return the categories 
    # where the user matches the person making the request.
    def get_queryset(self):
        # self.request.user contains the user who sent the JWT token.
        return Category.objects.filter(user=self.request.user)

    # We override "perform_create" to automatically set the user when a category is made.
    # The frontend shouldn't have to send "user_id=5"; the backend should figure it out securely!
    def perform_create(self, serializer):
        # Force the user field to be the logged-in user before saving to the database.
        serializer.save(user=self.request.user)


# =====================================================================
# TRANSACTION VIEWSET
# Handles full CRUD for financial transactions.
# =====================================================================
class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to perform CRUD operations on their transactions.
    Supports limit-offset pagination and filtering by date range.
    Restricted to authenticated users only.
    """
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    
    # Apply the built-in pagination. The frontend will request '?limit=10'.
    pagination_class = LimitOffsetPagination

    # Like the CategoryViewSet, we must filter so users only see their own transactions.
    def get_queryset(self):
        # 1. Start with only this user's transactions.
        # 2. Order them by date descending ('-date'), so newest is first.
        # 3. Add '-id' as a tie-breaker so transactions on the same day stay in consistent order.
        queryset = Transaction.objects.filter(user=self.request.user).order_by('-date', '-id')
        
        # We allow the frontend to filter by date ranges using the URL.
        # Example: /api/transactions/?start_date=2026-07-01
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        # If the user provided a start_date, filter transactions where the date is Greater Than or Equal To (gte) it.
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
            
        # If the user provided an end_date, filter transactions where the date is Less Than or Equal To (lte) it.
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
            
        # Return the final filtered, sorted, and isolated list of transactions back to DRF!
        return queryset

    # Just like categories, we automatically assign the transaction to the person creating it.
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
