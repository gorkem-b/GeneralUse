// SELF-DESTRUCT SERVICE WORKER
// This SW does ONE thing: destroys all caches and unregisters itself.
// Once all users have loaded this, the PWA cache trap is permanently broken.

self.addEventListener('install', () => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          console.log('[SW] Destroying cache:', cacheName);
          return caches.delete(cacheName);
        })
      );
    }).then(() => {
      console.log('[SW] All caches destroyed. Unregistering self...');
      return self.registration.unregister();
    }).then(() => {
      return self.clients.matchAll();
    }).then((clients) => {
      clients.forEach((client) => client.navigate(client.url));
    })
  );
});
