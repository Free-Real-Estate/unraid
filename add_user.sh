#!/bin/bash

docker stop files

filebrowser users add $1 $2 --scope /srv/$1 --locale fr

docker start files

docker run -d --restart unless-stopped --name $1 --net v1_free_real_estate -v $(pwd)/users/data/$1:/var/www/html:rw trafex/alpine-nginx-php7

docker run -d \
  --net fre_free_real_estate \
  --name=code-$1 \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Europe/Paris \
  -e PASSWORD=$2 \
  -v /home/fre/users/data/$1:/config/workspace \
  --restart unless-stopped \
  ghcr.io/linuxserver/code-server