const CACHE_NAME = 'shape-and-plate-cache-v1';
const urlsToCache = [
  '/',
  '/workout/',
  '/plate/',
  '/perfil/',
  '/static/css/base.css',
  '/static/js/theme.js',
  '/static/img/faviconblanco.png',
  '/static/navbar/dumbbell.svg',
  '/static/navbar/fork.svg',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.match(event.request).then((response) => {
        const fetchPromise = fetch(event.request).then((networkResponse) => {
          cache.put(event.request, networkResponse.clone());
          return networkResponse;
        });
        return response || fetchPromise;
      });
    })
  );
});