from django.db import models

class WeatherCache(models.Model):
    """
    Model for caching weather data to avoid hitting the Open-Meteo API too frequently.
    We save the latitude and longitude, along with the JSON response and a timestamp.
    """
    # Max digits 9 with 6 decimal places is standard for GPS coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    # Store the raw JSON data returned from the weather API
    weather_data = models.JSONField()
    
    # Automatically record exactly when this cache was created or updated
    fetched_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Prevent duplicate entries for the exact same location
        unique_together = ('latitude', 'longitude')
