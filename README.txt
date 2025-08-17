
SHOP MANAGER — FULL DJANGO PROJECT (MySQL + PWA + REST API + JWT)

Quick start:
1) Create MySQL DB:  CREATE DATABASE shop_manager_db;
2) Open shop_manager/settings.py and update:
   USER='root', PASSWORD='your_password', NAME='shop_manager_db'
3) Install packages:
   pip install django mysqlclient djangorestframework djangorestframework-simplejwt django-cors-headers pillow
4) Migrate & run:
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
5) Login:
   - Visit http://127.0.0.1:8000/accounts/login/ to sign in (custom login page)
   - Or http://127.0.0.1:8000/admin/ for Django admin

API auth:
- POST /api/token/ with username & password -> returns access & refresh
- Use Authorization: Bearer <access> for /api/products/ and /api/sales/

PWA:
- Manifest & Service Worker included (static/manifest.json and static/sw.js)
- Replace icons at static/inventory/icons/192.png and 512.png
- Use HTTPS in production for service worker, camera, and JWT security

Production notes:
- Set DEBUG=False, add ALLOWED_HOSTS
- Configure proper CORS (CORS_ALLOW_ALL_ORIGINS=False and set CORS_ALLOWED_ORIGINS)
- Serve static files with WhiteNoise or a web server, and store media on durable storage
