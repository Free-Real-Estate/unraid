# Docker compose for Free Real Estate!

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

Finally to add a new user simply run the following script

```sh
./add_user.sh <username> <password>
```

this will start the nginx-php docker under the `username.mydomain.com`  host and code-server under `code-username.mydomain.com` 