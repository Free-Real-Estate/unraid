#!/bin/python3

import os
import subprocess
import json
from sys import argv

config = {
    'code_image': 'ghcr.io/linuxserver/code-server',
    'users_data': '/home/pog/docker/test/v1/users/data/',
    'users_code_data': '/home/pog/docker/test/v1/users/code-data/',
    'web_image': 'trafex/alpine-nginx-php7',
    'web_image_volume': {
        'web_config': '/home/pog/docker/test/v1/nginx_user.conf'
    }
}

user_list = {}


def init_containerdb(userList):
    global user_list
    output = subprocess.getoutput('docker ps').split('\n')
    for index, line in enumerate(output, start=1):
        element_list = line.split()
        # print(element_list)
        if 'code-' in element_list[-1]:
            container_name = element_list[-1]
            if container_name[container_name.find('-')+1:] not in userList:
                user_name = container_name[container_name.find('-')+1:]
                userList[user_name] = {}
                userList[user_name]['code_container_name'] = element_list[-1]
                userList[user_name]['code_container_id'] = element_list[0]
                for index, line2 in enumerate(output, start=1):
                    element_list2 = line2.split()
                    if user_name == element_list2[-1]:
                        userList[user_name]['web_container_name'] = element_list2[-1]
                        userList[user_name]['web_container_id'] = element_list2[0]


def save_to_json(path):
    global user_list
    with open(path, 'w') as outfile:
        json.dump(user_list, outfile, indent=4)


def load_json(path):
    global user_list
    with open(path) as infile:
        user_list = json.load(infile)


def start_code(user):
    global user_list
    os.system('docker run -d --net=v1_free_real_estate --name=code-' + user + ' -e DOCKER_MODS=linuxserver/mods:code-server-php -e PUID=1000 -e PGID=1000 -e TZ=Europe/Paris -e HASHED_PASSWORD=' + user_list[user]['hash_pass'] + ' -v ' +
              config['users_code_data'] + user + ':/config -v ' + config['users_data'] + user + ':/config/workspace --restart unless-stopped ' + config['code_image'])
    user_list[user]['code_container_name'] = 'code-'+user
    user_list[user]['code_container_id'] = subprocess.getoutput(
        'docker ps -aqf "name=code-' + user + '"')
    print(user + ' vs-code started')


def start_web(user):
    global user_list
    os.system('docker run -d --restart=unless-stopped --name=' + user +
              ' --net=v1_free_real_estate -v ' + config['users_data'] + user + ':/var/www/html:rw -v '+config['web_image_volume']['web_config'] + ':/etc/nginx/nginx.conf ' + config['web_image'])

    user_list[user]['web_container_name'] = user
    user_list[user]['web_container_id'] = subprocess.getoutput(
        'docker ps -aqf "name=' + user + '"')
    print(user + ' web started')


def start_user(user):
    global user_list
    os.system('docker run -d --net=v1_free_real_estate --name=' + user + ' -e PUID=1000 -e PGID=1000 -e TZ=Europe/Paris -e HASHED_PASSWORD=' + user_list[user]['hash_pass'] + ' -v ' +
              config['users_code_data'] + user + ':/config -v ' + config['users_data'] + user + ':/config/workspace -v ' + config['web_image_volume']['web_config'] + ':/etc/nginx/nginx.conf ' ' --restart unless-stopped ' + "fre-user-docker:latest")
    user_list[user]['code_container_name'] = user
    user_list[user]['code_container_id'] = subprocess.getoutput(
        'docker ps -aqf "name=code-' + user + '"')
    print(user + ' vs-code started')
    print(user + ' containers started')


def start_user_old(user):
    global user_list
    start_web(user)
    start_code(user)
    print(user + ' containers started')


def stop_user(user):
    global user_list
    # os.system('docker rm -f ' + user_list[user]['web_container_name'])
    os.system('docker rm -f ' + user_list[user]['code_container_name'])
    print(user + ' containers stoped')


def add_user(user, password):
    global user_list
    os.system('docker stop files')
    os.system('filebrowser users add ' + user + ' ' +
              password + ' --scope /srv/' + user + ' --locale fr')
    os.system('docker start files')
    user_list[user] = {}
    user_list[user]['hash_pass'] = subprocess.getoutput(
        'echo -n \"' + password + '\" | sha256sum | cut -d\' \' -f1')
    start_user(user)
    os.system('sudo cp ./template/* ./users/data/' + user)
    os.system('sudo chmod a+rwx ./users/data/' + user + '/*')
    print(user + ' added')


def del_user(user):
    global user_list
    os.system('docker stop files')
    os.system('filebrowser users rm ' + user)
    os.system('docker start files')
    stop_user(user)
    os.system('sudo rm -rf ./users/data/' + user)
    del user_list[user]
    print(user + ' deleted')


def stop_all():
    global user_list
    for user in user_list.keys():
        stop_user(user)


def start_all():
    global user_list
    for user in user_list.keys():
        start_user(user)


def main():

    for nb, arg in enumerate(argv):
        if arg == "add":
            load_json('containerdb.json')
            add_user(argv[nb + 1], argv[nb + 2])

        if arg == "del":
            load_json('containerdb.json')
            del_user(argv[nb + 1])
        if arg == "start":
            load_json('containerdb.json')
            start_user(argv[nb + 1])
        if arg == "stop":
            load_json('containerdb.json')
            stop_user(argv[nb + 1])
        if arg == "start_all":
            load_json('containerdb.json')
            start_all()
        if arg == "stop_all":
            load_json('containerdb.json')
            stop_all()
        if arg == "rebuild_db":
            init_containerdb(user_list)
    save_to_json('containerdb.json')


if __name__ == "__main__":
    # execute only if run as a script
    main()
