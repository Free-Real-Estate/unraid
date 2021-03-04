# Docker compose for Free Real Estate! (Highly experimental)
## What is this about?

The following docker structure allows you to allocate one `nginx-php` and one `codeserver` docker instance per user. While using multiple dockers can highly decrease performance, it is a good way to completely separate PHP instances from one user to another.

All the dockers are linked to one reverse-proxy forwarding every `user.domain.com` and `code-user.domain.com` to their corresponding docker.

The current config is still in beta and also comes with a portainer instance and a redirect to an unraid panel. You really should not use this out of the box.

## Instalation

First you will need to create a few files in the repo directory:

- `filebrowser/filebrowser.db` file containing the file browser users information. Once created it will automatically be initialized by docker
- `letsencrypt/yourdomain/` and put your wildcard ssl certificates in there 

Then you'll need to edit the `nginx.conf` file in `./nginx/nginx.conf` and replace pau-cy.tech by your domain. You will also need to replace pau-cy.tech by your domain name in the `./nginx/conf.d/common.conf` 

Once evrything is done you can start the project with docker-compose

```sh
docker-compose up -d
```

the `filebrowser` application is also required on your host machine in order to be able to add an user while the docker is down. simply run those commands to install it

```sh
curl -fsSL https://filebrowser.org/get.sh | bash
mkdir -p /etc/filebrowser
cp filebrowser/.filebrowser.json /etc/filebrowser/
ln -s $(pwd)/filebrowser/filebrowser.db /etc/filebrowser/database.db
```

Finally to manage user you can use the `user_managment.py` script


this will start the nginx-php docker under the `username.mydomain.com`  host and code-server under `code-username.mydomain.com` 

### User managment script

first you will need to change a few things in the script config variable

The folder in wich the data of every user is stored :

```py
'users_data': '/home/pog/docker/test/v1/users/data/'
```

and the path to the user nginx config

```py
'web_image_volume': {
        'web_config': '/home/pog/docker/test/v1/nginx_user.conf'
}
```

#### Add user

```sh
./user_managment.py add <username> <password>
```

This will add the user to `filebrowser` and create a code-server and nginx-php instances for him

#### Del user

```sh
./user_managment.py del <username>
```

Remove the user from fileserver and remove his code-server and nginx-php instances

#### Start/Stop user web-server and code-server

```sh
./user_managment.py start/stop <username>
```

#### Start_all/Stop_all web-server and code-server

```sh
./user_managment.py start_all/stop_all
```