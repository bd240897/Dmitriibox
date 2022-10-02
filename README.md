https://github.com/bd240897/Dmitriibox

# Dmitrii Box

Игра Викторина

## ДИПЛОЙ НА https://cloud.yandex.ru

### Ветки

#### master
Главная ветка - не помню что тут сейчас

    git clone https://github.com/bd240897/Dmitriibox.git 

#### Django_channels
Проект на Django Templates + DRF (a little)

    git clone https://github.com/bd240897/Dmitriibox.git --branch Django_channels

#### vue
Проект на Vue.js + DRF

    git clone https://github.com/bd240897/Dmitriibox.git --branch vue

## Quickstart Start Linux
    sudo apt-get update
    sudo apt-get install -y git python3-dev python3-venv python3-pip supervisor nginx vim libpq-dev

# Python version 3.8
### Install Python3.8
https://infoit.com.ua/linux/kak-ustanovit-python-3-8-na-debian-10/

    sudo apt update
    sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
    cd ~/opt
    sudo wget https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tar.xz
    sudo tar -xf Python-3.8.2.tar.xz
    cd Python-3.8.2
    sudo ./configure --enable-optimizations
    sudo make -j 2
    sudo make altinstall
    python3.8 --version

# Install Postgres
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04-ru
anather instuction
https://www.youtube.com/watch?v=FLiKTJqyyvs

    sudo apt install -y postgresql postgresql-contrib
    sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
    sudo -u postgres psql
    CREATE DATABASE DmitriiBox;
    CREATE USER amid WITH PASSWORD '1234qwer';
    ALTER ROLE amid SET client_encoding TO 'utf8';
    ALTER ROLE amid SET default_transaction_isolation TO 'read committed';
    ALTER ROLE amid SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE DmitriiBox TO amid;
    \q
    //test
    \list - list bd '\l'
    \connect dmitriibox; - connect '\c name'
    \dt - list table
    SELECT * FROM auth_user;


#### run test project
    cd ~/home/amid/
    git clone https://github.com/bd240897/Dmitriibox.git 
    cd DmitriiBox

    python3.8 -m venv venv   
    source venv/bin/activate
    pip install --upgrade pip
    pip3 install -r requirements.txt
    python manage.py runserver 0.0.0.0:8001

Run the app with gunicorn:

    gunicorn game_muster.wsgi -b 0.0.0.0:8000
    // gunicorn game_muster.wsgi -b 127.0.0.1:8001

Collect static files:

    python3 manage.py collectstatic 

### Setup NGINX:

    sudo nano /etc/nginx/sites-enabled/default
    
Config file:

    server {
            listen 80 default_server;
            listen [::]:80 default_server;

            location /static/ {
                alias /home/user/game_muster/static/; 
            }

            location / {
                proxy_pass http://127.0.0.1:8001;
                proxy_set_header X-Forwarded-Host $server_name;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_redirect off;
                add_header P3P 'CP="ALL DSP COR PSAa OUR NOR ONL UNI COM NAV"';
                add_header Access-Control-Allow-Origin *;
            }
    }
    
Restart NGINX:
    
    sudo service nginx restart
    
    
### Setup Supervisor:

    sudo nano /etc/supervisor/conf.d/game_muster.conf

Config file:
    
    [program:game_muster]
    command = /home/user/game_muster/venv/bin/gunicorn game_muster.wsgi  -b 127.0.0.1:8000 -w 4 --timeout 90
    autostart=true
    autorestart=true
    directory=/home/user/game_muster 
    stderr_logfile=/var/log/game_muster.err.log
    stdout_logfile=/var/log/game_muster.out.log
    
Update supervisor with the new process:
    
    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl status game_muster
    sudo supervisorctl stop game_muster
    
To restart the process after the code updates run:

    sudo supervisorctl restart game_muster

notes
    twisted-iocpsupport==1.0.2 - onle for Windows (delete from req.txt!)

 