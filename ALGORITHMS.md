# GeneralUse: Core System Algorithms

This document defines the mathematical models, logic constraints, and pseudocode algorithms that govern the operations of the **GeneralUse** system.

---

## 1. Authentication & Session Security (JWT Flow)
Manages user authentication and view routing using JSON Web Tokens (JWT) with asymmetric expirations.

### Algorithm 1: Client-Side Route Guarding
```
Input: Target Route (to), Current Route (from)
Output: Route transition allowed OR redirect to auth page

1. Retrieve access_token from localStorage.
2. If access_token is empty or invalid:
       Call verifyToken() to check if token exists:
           Read access_token
           If missing -> set isAuthenticated = false
3. If to.meta.requiresAuth is True AND isAuthenticated is False:
       Redirect browser to '/login'
4. Else If to.path is '/login' AND isAuthenticated is True:
       Redirect browser to '/' (Finance Center)
5. Else:
       Allow routing transition.
```

### Algorithm 2: Global API Token Interception & 401 Expiration Handling
```
Input: HTTP Request Object (req), HTTP Response Object (res)
Output: Outgoing Request with headers OR Session Redirection

[Request Interception Stage]
1. Read access_token from localStorage.
2. If access_token is present:
       Attach Authorization header: "Bearer " + access_token

[Response Interception Stage]
1. If res.status == 401 (Unauthorized):
       Remove access_token from localStorage
       Remove refresh_token from localStorage
       If current_path != '/login':
           Redirect browser to '/login'
2. Return Response or Reject promise with error details.
```

---

## 2. Weather Engine (City Geocoding & Caching Proxy)
Avoids browser location tracking and shields external API from excessive requests.

### Algorithm 3: Manual City Geocoding
```
Input: City Name String (cityName)
Output: Weather JSON Data or Exception

1. Send GET request to Open-Meteo Geocoding API:
   https://geocoding-api.open-meteo.com/v1/search?name={cityName}&count=1
2. If HTTP Response is successful AND results array is not empty:
       Extract latitude, longitude, and name from results[0]
       Save name, latitude, longitude to localStorage
       Trigger Algorithm 4 (fetchWeather) using latitude and longitude
3. Else:
       Set weatherStore.error = "City not found"
```

### Algorithm 4: Weather Caching Proxy (Backend)
```
Input: Coordinates (lat, lon)
Output: Current Weather JSON

1. Round coordinates to 1 decimal place:
       exact_lat = round(Decimal(lat), 1)
       exact_lon = round(Decimal(lon), 1)
2. Define time_threshold = CurrentTime - 30 minutes
3. Search DB: WeatherCache.objects.filter(
       latitude=exact_lat, 
       longitude=exact_lon, 
       fetched_at >= time_threshold
   )
4. If fresh cache record is found:
       Return cached weather_data immediately.
5. Else:
       Try:
           Send GET request:
           https://api.open-meteo.com/v1/forecast?latitude={exact_lat}&longitude={exact_lon}&current_weather=true
           Extract data = response.json().get('current_weather')
           Save/Update record in DB with exact_lat, exact_lon, data, fetched_at=now
           Return data
       Catch API Exception:
           Search DB for newest record matching exact_lat, exact_lon (ignoring age limit)
           If stale record is found:
               Return stale weather_data
           Else:
               Return HTTP 503 Service Unavailable (Error)
```

---

## 3. Real-Time Notification Polling
Performs long-polling with strict request spacing and circuit-breaker handling.

### Algorithm 5: Safe Polling & Rate Mitigation
```
Input: isPolling flag (Boolean)
Output: Real-time notification lists

1. On App Mount:
       If isPolling is True -> Terminate setup (polling already running)
       Set isPolling = True
2. Loop: While isPolling is True:
       Try:
           Send API request: GET /api/notifications/poll/
           If response contains notification items:
               Push items to notifications array
               Send POST /api/notifications/mark-read/ with items IDs
           Await a setTimeout Promise for exactly 5000ms.
       Catch Error:
           If Error.status == 401 (Unauthorized):
               Set isPolling = False (Exit loop)
               Trigger Algorithm 2 (Authentication redirection)
           Else:
               Await a setTimeout Promise for 5000ms.
```

---

## 4. Finance Ledger (Local Store Aggregation)
Calculates real-time values dynamically from the loaded transaction array.

### Algorithm 6: Local Dynamic Filtering & Math Calculations
```
Input: selectedDateFilter ('ALL', 'THIS_MONTH', 'LAST_30', 'THIS_YEAR')
Output: activeTransactions Array, totalIncome, totalExpense, netBalance

1. Evaluate activeTransactions:
       Let now = CurrentDate()
       Return transactions.filter(t => {
           t_date = Date(t.date)
           If selectedDateFilter == 'THIS_MONTH':
               return t_date.Month == now.Month AND t_date.Year == now.Year
           If selectedDateFilter == 'LAST_30':
               return t_date > (now - 30 days)
           If selectedDateFilter == 'THIS_YEAR':
               return t_date.Year == now.Year
           If selectedDateFilter == 'ALL':
               return True
       })
2. Calculate totalIncome:
       Return activeTransactions.filter(t => t.type == 'INCOME')
                               .reduce((sum, t) => sum + t.amount, 0)
3. Calculate totalExpense:
       Return activeTransactions.filter(t => t.type == 'EXPENSE')
                               .reduce((sum, t) => sum + t.amount, 0)
4. Calculate netBalance:
       Return totalIncome - totalExpense
```

---

## 5. Notes Matrix Document Engine
Handles document caching and duplicate prevention.

### Algorithm 7: Contextual Note Duplicate Guard
```
Input: Note Object (noteData)
Output: Saved Note Object or Validation Exception

1. If noteData.id is present:
       Send PUT /api/dashboard/notes/{id}/ to update existing record
       Find index of note in local items array and update it
2. If noteData.id is NOT present (New Note Draft):
       Send validated data to backend: POST /api/dashboard/notes/
       In Backend View:
           Read content = validated_data.get('content', '')
           If content is NOT empty:
               time_threshold = now - 1 minute
               Check DB: Note.objects.filter(user, content, created_at >= time_threshold)
               If duplicate record is found:
                   Raise ValidationError (HTTP 400 Bad Request)
           Save note to database associated with request.user
       If Save Successful:
           Push response note object to local items array
           Set activeNoteId = response.id
```
