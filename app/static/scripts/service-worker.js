const CACHE_NAME = "schueler-firma-cache-v1";
const urlsToCache = [
  "/",
  "/login",
  "/logout",
  "/impressum",
  "/manifest.json",
  "/static/style/style.css",
  "/static/img/back.png",
  "/admin/dashboard",
  "/admin/sell",
  "/admin/tables",
  "/admin/new-product",
  "/admin/search-product",
  "/admin/settings",
  "/404.html",
  "/403.html",
  "app/static/img/favicon/apple-touch-icon.png",
  "app/static/img/favicon/favicon-16x16.png",
  "app/static/img/favicon/favicon-32x32.png"
];

// Installations-Event: Cache anlegen
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
  self.skipWaiting();
});

// Aktivierungs-Event: Alte Caches löschen
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((cacheNames) =>
        Promise.all(
          cacheNames
            .filter((name) => name !== CACHE_NAME)
            .map((name) => caches.delete(name))
        )
      )
  );
  self.clients.claim();
});

// Fetch-Event: Versuche aus dem Cache zu laden, sonst aus dem Netz
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return (
        response ||
        fetch(event.request).catch(() =>
          // Optional: Fallback-Seite für offline
          caches.match("/")
        )
      );
    })
  );
});
