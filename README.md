# Docker compose for Free Real Estate!

## Instalation

first you'll need to create a few files in the repo directory:

- `filebrowser/filebrowser.db` file containing the file browser users information. Once created it will automatically be initialized by docker
- `letsencrypt/yourdomain/` and put your wildcard ssl certificates in there 

Then you'll need to edit the `nginx.conf` file in `./nginx/nginx.conf` and replace pau-cy.tech by your domain. You will also need to replace pau-cy.tech by you're domain name in the `./nginx/conf.d/common.conf` 

once evrything is done you can start the project with docker-compose

```sh
docker-compose up -d
```

the `filebrowser` application is also required to be installed on your host machine to be able to add user will the docker is down. simply run those command to install it

```sh
curl -fsSL https://filebrowser.org/get.sh | bash
mkdir -p /etc/filebrowser
cp filebrowser/.filebrowser.json /etc/filebrowser/
ln -s $(pwd)/filebrowser/filebrowser.db /etc/filebrowser/database.db
```

Finally to add a user simply run the following script in the 

```sh
./add_user.sh <username> <password>
```

this will start the nginx-php docker under the `username.mydomain.com`  host and code-server under `code-username.mydomain.com` 