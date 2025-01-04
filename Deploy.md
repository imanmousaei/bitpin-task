# Django Deployment on Ubuntu with Nginx & Gunicorn

## User
### create user with sudo access named 'iman':
`useradd -m -s /bin/bash -G sudo iman`
### change password of iman:
`passwd iman`

---

## Nginx
### install nginx : 
```
apt-get update
apt-get install nginx
```

### create a file for site's config:
```
cd /etc/nginx/sites-available/
vim bitpin.com
```

### copy this in that file(replace IP_PLACEHOLDER with actual IP of the server):
```
server{
    listen 80;
    server_name IP_PLACEHOLDER bitpin.com;
    
    location /static/ {
        alias /home/bitpin/static/;
    } 
    
    location / {
        proxy_pass http://localhost:8000;
    }
}
```

### then use that file in sites-enabled:
```
cd ../sites-enabled/
ln -s /etc/nginx/sites-available/bitpin.com
```
---

## PostgreSQL

### install postgres:
`apt-get -y install postgresql`

### create user for postgres:
`sudo -u postgres createuser --interactive`

### create database with the name of your django settings:
```bash
sudo -u postgres createdb -O postgres bitpindb
sudo -u postgres psql -l
```

### change password of db user : 
```bash
sudo -u postgres psql bitpindb
ALTER USER postgres WITH PASSWORD 'psq1234';
```
---

## Gunicorn : 

### create a file to set up a service:
```bash
cd /etc/systemd/system
vim gunicorn.service
```

### copy this into the file : 
```
[Unit]
Description=Django Lessons

[Service]
Type=simple
PIDFile=/home/bitpin/gunicorn.pid
User=root
Group=root
EnvironmentFile=/etc/lessons/gunicorn.env
WorkingDirectory=/home/bitpin
ExecStart=/home/bitpin/venv/bin/gunicorn --config=/etc/lessons/gunicorn.conf.py bitpin.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
```

### then to config it:
```bash
cd /etc
mkdir lessons
cd lessons/
vim gunicorn.conf.py
```

### copy this into the file: 
```bash
workers = 2
syslog = True
bind = ['0.0.0.0']
umask = 0
loglevel = 'info'
user = 'root'
group = 'root'
```
---

## Django
### create virtual environment for the project:
```bash
cd bitpin
apt-get install python3-venv
python3 -m venv venv
```

### activate venv:
`source venv/bin/activate`

### install dependencies in venv:
`pip3 install -r requirements.txt`

### add static & media urls in django urls.py:
```
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### at last tell django to collectstatic:
`python3 manage.py collectstatic`
