#!/usr/bin/env bash

# Instala lo necesario
apt-get update
apt-get -y upgrade
# apt-get install -y python3-pip
apt-get install -y postgresql
apt-get install -y postgis
apt-get install -y git
apt-get install -y redis-server
apt-get install -y python3-tk
apt-get install -y gdal-bin
apt-get install -y libgdal-dev
apt-get install -y supervisor
apt-get install -y nginx

# Incrementa memoria del broker de mensajes y lo inicializa
echo "maxmemory 128mb" >> /etc/redis/redis.conf
echo "maxmemory-policy allkeys-lru" >> /etc/redis/redis.conf
echo "supervised systemd" >> /etc/redis/redis.conf

systemctl enable redis-server.service

locale-gen es
update-locale

# Crea la base de datos
-u postgres createdb geo
-u postgres psql -U postgres -d postgres -c "alter user postgres with password 'contra';"
-u postgres psql -U postgres -d postgres -c "CREATE EXTENSION postgis;"
# Descarga la aplicacion y la instala
# git clone https://marcojulio:moam880818@bitbucket.org/marcojulio/imss.git /home/ubuntu/
# pip3 install -r requirements.txt
cd /home/ubuntu/imss
cp /home/ubuntu/imss/imss_celery.conf /etc/supervisor/conf.d/
cp /home/ubuntu/imss/imss_celerybeat.conf /etc/supervisor/conf.d/
touch /var/log/celery/imss_worker.log
touch /var/log/celery/imss_beat.log

# Configura el supervisor de Celery
# supervisorctl reread
# supervisorctl update
# supervisorctl start imssworker

# Migra la base de datos
python3 manage.py makemigrations
python3 manage.py migrate

# Copia el archivo de configuracion de nginx y corre gunicorn
cp /home/ubuntu/imss/default /etc/nginx/sites-enabled/
# python3 manage.py corre_gunicorn
# python3 manage.py ogrinspect shp/30ent.shp Entidad --mapping --multi >> geo/models.py
# python3 manage.py ogrinspect shp/30l.shp Localidad --mapping --multi >> geo/models.py
# python3 manage.py ogrinspect shp/30m.shp Manzana --mapping --multi >> geo/models.py
# python3 manage.py ogrinspect shp/30a.shp Agebu --mapping --multi >> geo/models.py
# python3 manage.py ogrinspect shp/30ar.shp Agebr --mapping --multi >> geo/models.py
# python3 manage.py ogrinspect Colonias/30m.shp Colonia --mapping --multi >> geo/models.py
