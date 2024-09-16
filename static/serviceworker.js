const CACHE_NAME = 'shape-and-plate-cache-v3';
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

const DB_RELATED_URLS = [
  '/data_preview',
  '/generate_workout',
  '/plate',
  '/profile',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(fetch(event.request));
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});