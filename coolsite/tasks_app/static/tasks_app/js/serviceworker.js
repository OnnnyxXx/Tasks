//var staticCacheName = "django-pwa-v" + new Date().getTime();
//// Список файлов для кэширования (пустой, так как мы не используем кэш)
//var filesToCache = [];
//
//
//self.addEventListener('install', function(event) {
//    // Пропускаем шаг кэширования
//    event.waitUntil(self.skipWaiting());
//});
//
//
//self.addEventListener('activate', function(event) {
//
//    event.waitUntil(
//        caches.keys().then(function(cacheNames) {
//            return Promise.all(
//                cacheNames.map(function(cacheName) {
//                    return caches.delete(cacheName);
//                })
//            );
//        }).then(function() {
//            return self.clients.claim();
//        })
//    );
//});
//
//
//self.addEventListener('fetch', function(event) {
//    event.respondWith(fetch(event.request));
//});
//
//
//
//
//
//
////
////var staticCacheName = "django-pwa-v" + new Date().getTime();
//////Нужно будет расширить
////var filesToCache = [
////    '/',
////
////
////
////];
////
////
////self.addEventListener('fetch', function(event) {
////    event.respondWith(
////        caches.open(staticCacheName).then(function(cache) {
////            return cache.match(event.request).then(function(response) {
////                var fetchPromise = fetch(event.request).then(function(networkResponse) {
////                    // Обновляем кэш, если мы получили новый контент
////                    if (networkResponse) {
////                        cache.put(event.request, networkResponse.clone());
////                    }
////                    return networkResponse;
////                });
////                // Используем кэшированный ответ, если он доступен
////                return response || fetchPromise;
////            });
////        })
////    );
////});
////
////// Clear cache on activate
////self.addEventListener('activate', event => {
////    event.waitUntil(
////        caches.keys().then(cacheNames => {
////            return Promise.all(
////                cacheNames
////                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
////                    .filter(cacheName => (cacheName !== staticCacheName))
////                    .map(cacheName => caches.delete(cacheName))
////            );
////        })
////    );
////});
////
////// Serve from Cache
////self.addEventListener("fetch", event => {
////    event.respondWith(
////        caches.match(event.request)
////            .then(response => {
////                return response || fetch(event.request);
////            })
////            .catch(() => {
////                return caches.match('offline');
////            })
////    )
////});