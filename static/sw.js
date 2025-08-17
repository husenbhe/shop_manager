
const CACHE_NAME = 'burhani-shop-v1';
const ASSETS = [
  '/',
  '/static/inventory/css/style.css',
  '/static/inventory/icons/192.png',
  '/static/inventory/icons/512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(fetch(event.request).catch(() => caches.match(event.request)));
    return;
  }
  event.respondWith(
    caches.match(event.request, { ignoreSearch: true }).then(resp => resp || fetch(event.request))
  );
});
