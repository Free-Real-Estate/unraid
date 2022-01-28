#!/bin/sh

export $(grep -v '^#' ../.env)

docker run \
  --name=$1 \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=${TZ} \
  -e PASSWORD=$2 \
  -e DOCKER_MODS="linuxserver/mods:code-server-extension-arguments" \
  -e VSCODE_EXTENSION_ID="yandeu.five-server|bmewburn.vscode-intelephense-client" \
  -v $(pwd)/../data/users/$1/.code:/config \
  -v $(pwd)/../data/users/$1/site:/config/workspace \
  --network fre-ng_fre \
  --label traefik.http.routers.$1-code.rule=Host\(\`$1-code.${DOMAIN}\`\) \
  --label traefik.http.services.$1-code.loadbalancer.server.port=8443 \
  --label traefik.http.routers.$1-code.service=$1-code \
  --label traefik.http.routers.$1.rule=Host\(\`$1.${DOMAIN}\`\) \
  --label traefik.http.services.$1.loadbalancer.server.port=80 \
  --label traefik.http.routers.$1.service=$1 \
  --rm docker.io/fre/code-php
