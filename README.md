# Docker compose for Free Real Estate! (Highly experimental)
## What is this about?

The following docker structure allows you to allocate one `nginx-php` and one `codeserver` docker instance per user. While using multiple dockers can highly decrease performance, it is a good way to completely separate PHP instances from one user to another.

All the dockers are linked to one reverse-proxy forwarding every `user.domain.com` and `code-user.domain.com` to their corresponding docker.

The current config is still in beta and also comes with a portainer instance and a redirect to an unraid panel. You really should not use this out of the box.

## Instalation

First build the custom code-server image

```sh
docker build -t fre/code-php -f Dockerfile https://github.com/Free-Real-Estate/code-nginx-php-docker.git
```
