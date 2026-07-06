# GeneralUse: Advanced Productivity Hub

Welcome to the **GeneralUse** project (formerly SpendingTracker)! This project has been heavily refactored from a simple monolithic Django application into a professional, decoupled, modern Web Application serving as a Personal Productivity Dashboard. 

## 🚀 The Architecture

This project is built using a decoupled **Django REST Framework** backend and a **Vue.js 3** frontend. We have implemented several advanced architectural patterns to ensure scalability, security, and maintainability.

### 1. The Domain-Driven Design (Backend)
The backend is split into independent "Domain Apps" rather than a single monolith.
- `core`: The central project configuration and global routing.
- `finance`: The core expense tracking engine.
- `tasks`: A micro-applet for managing to-do lists.
- `notes`: A micro-applet for saving markdown notes.
- `events`: A micro-applet for scheduling reminders.
- `weather`: A micro-applet for fetching geolocation-based weather data.
- `notifications`: The central engine for managing long-polling in-app alerts.

### 2. The Service & Selector Layers (MVC Separation)
To avoid the notorious "Fat View" anti-pattern in Django, we have implemented strict separation of concerns:
- **Controllers (`views.py`)**: Responsible ONLY for parsing HTTP requests, checking permissions, and returning HTTP responses.
- **Service Layer (`services.py`)**: Encapsulates all complex Business Logic, Side Effects, and Data Mutations. This includes anti-spam validation and generating cross-domain notifications.
- **Selector Layer (`selectors.py`)**: A form of the Repository Pattern. All complex ORM queries, filtering, and data retrieval live here.

### 3. Data Integrity & Security
- **Soft Deletion**: Instead of permanently deleting records (`DELETE FROM...`), we use an `is_deleted` boolean flag. We created a custom `ActiveManager` that automatically filters out deleted records at the ORM level.
- **Anti-Spam Controls**: Overriding the `perform_create` method with business rules to block rapid identical submissions from bots or accidental double-clicks.
- **Rate Limiting**: Configured global API Throttling using `AnonRateThrottle` (10/min) and `UserRateThrottle` (100/min).

### 4. High-Performance Event Reminders
Instead of using heavy background workers (like Celery or APScheduler) to send emails, we designed an elegant in-app Notification engine.
- Reminders are created by setting a `Notification`'s `created_at` to a future date.
- The frontend connects to a spaced **Polling API** (`/api/notifications/poll/`) that runs efficiently every 5 seconds without locking up the database. It features an automated 401 circuit breaker that halts polling and redirects users to login when access tokens expire.

### 5. Progressive Web App (PWA) Installability
- **Manifest Integration**: Configured Web App Manifest (`manifest.json`) letting mobile browsers download and launch the app in standalone fullscreen mode.
- **Service Worker Offline Cache**: Implemented a custom caching thread (`sw.js`) utilizing a Cache-First-with-Network-Fallback strategy to load the app instantly and bypass API queries.

### 6. The Modern Vue.js Frontend
- **Pinia State Management**: Global state is elegantly managed using Pinia stores (`financeStore`, `tasksStore`, `notificationsStore`, etc).
- **Componentization**: Extracted reusable UI building blocks (`BaseCard`, `BaseButton`, `BaseInput`) to enforce consistency.
- **Glassmorphism UI**: Styled completely with Tailwind CSS, leveraging backdrop filters, gradients, and subtle borders to achieve a premium, dark-mode aesthetic.
- **Vue Transitions**: Implemented `<TransitionGroup>` for buttery smooth entry/exit animations when manipulating lists.

### 7. Documentation & Deployment Assets
- **Algorithm Specifications**: Standard pseudocode maps for session security, geocoding proxies, dynamic balance calculations, and polling loops are available inside [ALGORITHMS.md]
- **Deployment Hardening**: Enabled production settings (HSTS, SSL redirects, and proxy SSL headers for Oracle Cloud) under `settings.py` when `DEBUG = False`. Integrated `vercel.json` rewrites for Vercel SPA routing.

## 🛠️ How to Run Locally

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install the dependencies (requires Python 3.10+):
   ```bash
   pip install -r requirements.txt
   ```
3. Run database migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. Open the provided `localhost` link in your browser!
