#!/bin/sh

docker exec file-server filebrowser users add $1 $2 --scope /srv/$1 --locale fr
