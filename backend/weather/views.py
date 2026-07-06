import datetime
import requests
from decimal import Decimal
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import WeatherCache

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weather_proxy(request):
    """
    Controller (View) that handles HTTP parsing, caching, and external API fetching.
    """
    try:
        lat = float(request.query_params.get('lat'))
        lon = float(request.query_params.get('lon'))
    except (TypeError, ValueError):
        return Response({"error": "Invalid latitude or longitude"}, status=400)
    
    exact_lat = round(Decimal(lat), 1)
    exact_lon = round(Decimal(lon), 1)
    
    # 1. Try to get fresh cache (within 30 mins)
    threshold = timezone.now() - datetime.timedelta(minutes=30)
    fresh_cache = WeatherCache.objects.filter(
        latitude=exact_lat, 
        longitude=exact_lon, 
        fetched_at__gte=threshold
    ).first()
    
    if fresh_cache:
        return Response(fresh_cache.weather_data)
        
    # 2. If no cache, fetch from API
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={exact_lat}&longitude={exact_lon}&current_weather=true"
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json().get('current_weather', {})
        
        # Save fresh data to database cache
        WeatherCache.objects.update_or_create(
            latitude=exact_lat,
            longitude=exact_lon,
            defaults={'weather_data': data, 'fetched_at': timezone.now()}
        )
        return Response(data)
    except Exception:
        # 3. If API fails, fallback to stale cache
        stale_cache = WeatherCache.objects.filter(
            latitude=exact_lat, 
            longitude=exact_lon
        ).order_by('-fetched_at').first()
        
        if stale_cache:
            return Response(stale_cache.weather_data)
            
        return Response({"error": "Failed to fetch weather data"}, status=503)
