// Service Worker для CyberOrg PWA
const CACHE_NAME = 'cyberorg-v1.0.0';
const STATIC_CACHE_NAME = 'cyberorg-static-v1.0.0';

// Файлы для кэширования
const STATIC_FILES = [
    '/',
    '/static/css/style.css',
    '/static/css/webinars.css',
    '/static/images/logo.png',
    '/static/images/favicon.png',
    '/static/images/icon-192x192.png',
    '/static/images/icon-512x512.png',
    '/static/manifest.json',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap'
];

// Установка Service Worker
self.addEventListener('install', event => {
    console.log('Service Worker: Установка...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE_NAME)
            .then(cache => {
                console.log('Service Worker: Кэширование статических файлов');
                return cache.addAll(STATIC_FILES);
            })
            .then(() => {
                console.log('Service Worker: Установка завершена');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('Service Worker: Ошибка при установке', error);
            })
    );
});

// Активация Service Worker
self.addEventListener('activate', event => {
    console.log('Service Worker: Активация...');
    
    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => {
                        if (cacheName !== STATIC_CACHE_NAME && cacheName !== CACHE_NAME) {
                            console.log('Service Worker: Удаление старого кэша', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('Service Worker: Активация завершена');
                return self.clients.claim();
            })
    );
});

// Перехват запросов
self.addEventListener('fetch', event => {
    // Пропускаем запросы, которые не являются GET
    if (event.request.method !== 'GET') {
        return;
    }
    
    // Пропускаем запросы к внешним API
    if (event.request.url.includes('/api/') || 
        event.request.url.includes('googleapis.com') ||
        event.request.url.includes('gstatic.com')) {
        return;
    }
    
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Если файл найден в кэше, возвращаем его
                if (response) {
                    console.log('Service Worker: Запрос из кэша', event.request.url);
                    return response;
                }
                
                // Иначе делаем запрос к сети
                return fetch(event.request)
                    .then(response => {
                        // Проверяем, что ответ валидный
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }
                        
                        // Клонируем ответ для кэширования
                        const responseToCache = response.clone();
                        
                        // Кэшируем только статические ресурсы
                        if (event.request.url.includes('/static/') || 
                            event.request.url.includes('.css') ||
                            event.request.url.includes('.js') ||
                            event.request.url.includes('.png') ||
                            event.request.url.includes('.jpg') ||
                            event.request.url.includes('.jpeg') ||
                            event.request.url.includes('.gif') ||
                            event.request.url.includes('.svg')) {
                            
                            caches.open(STATIC_CACHE_NAME)
                                .then(cache => {
                                    cache.put(event.request, responseToCache);
                                });
                        }
                        
                        return response;
                    })
                    .catch(error => {
                        console.log('Service Worker: Ошибка сети', error);
                        
                        // Если это HTML страница, показываем офлайн страницу
                        if (event.request.headers.get('accept').includes('text/html')) {
                            return caches.match('/offline.html');
                        }
                        
                        // Для других ресурсов возвращаем ошибку
                        throw error;
                    });
            })
    );
});

// Обработка push уведомлений (для будущего использования)
self.addEventListener('push', event => {
    console.log('Service Worker: Получено push уведомление');
    
    const options = {
        body: event.data ? event.data.text() : 'Новое уведомление от CyberOrg',
        icon: '/static/images/icon-192x192.png',
        badge: '/static/images/icon-72x72.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'explore',
                title: 'Открыть',
                icon: '/static/images/icon-96x96.png'
            },
            {
                action: 'close',
                title: 'Закрыть',
                icon: '/static/images/icon-96x96.png'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('CyberOrg', options)
    );
});

// Обработка кликов по уведомлениям
self.addEventListener('notificationclick', event => {
    console.log('Service Worker: Клик по уведомлению');
    
    event.notification.close();
    
    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});
