"""
URL configuration for the backend Django project.

Think of urls.py like a phone book for your website. 
When a browser asks for "http://localhost:8000/api/categories/", 
this file decides which piece of Python code should run.
"""
from django.contrib import admin
from django.urls import path, include

# Import the JWT views provided by the simplejwt library.
# These handle user authentication tokens (logins and refreshing access).
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Import the DefaultRouter from DRF.
# Because we used "ViewSets" in views.py, we don't have to write URLs for GET, POST, PUT, DELETE.
# The router automatically writes all those URLs for us!
from rest_framework.routers import DefaultRouter

# Import our custom views (the Python code that handles the requests)
from finance.views import RegisterView, CategoryViewSet, TransactionViewSet

# 1. Create a new Router object.
router = DefaultRouter()

# 2. Register our ViewSets with the router.
# This says: "Whenever a request comes to /categories/, send it to the CategoryViewSet."
router.register(r'categories', CategoryViewSet, basename='category')

# This says: "Whenever a request comes to /transactions/, send it to the TransactionViewSet."
router.register(r'transactions', TransactionViewSet, basename='transaction')

# 3. Define the actual URL patterns (the list of routes our app responds to).
urlpatterns = [
    # The built-in Django admin panel (http://localhost:8000/admin/)
    path('admin/', admin.site.urls),
    
    # The registration endpoint (http://localhost:8000/api/register/)
    # We use .as_view() because RegisterView is a class, but urls.py needs a function.
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    
    # The login endpoint (http://localhost:8000/api/token/)
    # If the user sends correct credentials here, they get a JWT back.
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # The token refresh endpoint (http://localhost:8000/api/token/refresh/)
    # If an access token expires, use the refresh token to get a new one.
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # The router URLs. We include ALL the URLs the router automatically generated for us
    # under the 'api/' prefix. So we get:
    # GET /api/categories/
    # POST /api/categories/
    # GET /api/transactions/
    # etc...
    path('api/', include(router.urls)),
    
    # ---------------------------------------------------------
    # NEW DASHBOARD URLS (Weather, Notes, Tasks, Events)
    # ---------------------------------------------------------
    # This includes all the routes from our new dashboard app.
    path('api/dashboard/tasks/', include('tasks.urls')),
    path('api/dashboard/notes/', include('notes.urls')),
    path('api/dashboard/events/', include('events.urls')),
    path('api/dashboard/weather/', include('weather.urls')),
    path('api/notifications/', include('notifications.urls')),
]
