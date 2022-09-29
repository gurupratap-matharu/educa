Veer we take the following steps while setting up new Digital Ocean Droplet
We have followed this guide to setup: https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04


1. Add the public ip of the droplet to our ~/.ssh/config file for direct login
2. Once logged in as root run 
    - sudo apt update && sudo apt upgrade && sudo apt autoremove

3. Create normal User and grant administrative privileges
    - adduser veer
    - usermod -aG sudo veer

4. Copy authorized keys from root .ssh folder to our users .ssh folder so that we can
login directly via ssh as a normal user
    - rsync --archive --chown=veer:veer ~/.ssh /home/veer

5. Check/enable firewall and allowed apps
    ```
    ufw app list
    ufw allow OpenSSH
    ufw enable
    ufw status
    ```

   VIMP - Allow firewall to pass traffic to nginx app on port 80

   `sudo ufw allow 'Nginx Full'`

   then check `sudo ufw status` and you should see the Nginx app!
   temporarily allow incoming traffic to port 8000

   `sudo ufw allow 8000`

  now disable incoming traffic to port 8000
   `sudo ufw delete allow 8000`

Now Server setup is done. We use our normal user to setup django, nginx, and postgres

5. Install libraries
    - sudo apt update
    - sudo apt install python-pip python-dev libpq-dev postgresql postgresql-contrib nginx curl

6. Install pyenv
    - sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl

    - `curl https://pyenv.run | bash`
    - Add pyenv to path in .bashrc
    - pyenv update
    - install a python version by running `pyenv install -v 3.9.2`

### Install Poetry

    - curl -sSL https://install.python-poetry.org | python3 -
    - Add poetry to path `export PATH="/home/veer/.local/bin:$PATH"`

### Install Postgres user and db

    - sudo -u postgres psql
    - CREATE DATABASE myproject;
    - CREATE USER myprojectuser WITH PASSWORD 'password';
    - ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
    - ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
    - ALTER ROLE myprojectuser SET timezone TO 'UTC';
    - GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;

### Github SSH

    - Here veer just create a ssh private-public key pair and upload it to your github profile
    - this way you can clone your git repo via ssh

### Live App

Remember Veer these key points

to see your app live in a browser
    - make sure you have the port enabled in ufw firewall like port 80, 443, 8000
    - run django on 0.0.0.0 address and not on 127.0.0.1
    - run collect static command
 
### Systemmd Socket and Service files for Gunicorn

Veer first test running gunicorn locally from the command line in non-daemon mode
you should be able to see your app live from a browser
Once this checkpoint is achieved we

- create a gunicorn socket at boot that will listen for connections
    - when a connections occurs systemd will automatically start the gunicorn process to handle the connection


`sudo vim /etc/systemd/system/gunicorn.socket`

Add the following contents to it

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```


`sudo vim /etc/systemd/system/gunicorn.service`

Add the following contents to it

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=veer
Group=www-data
WorkingDirectory=/home/veer/code/myprojectdir
ExecStart=/home/veer/code/myprojectdir/myprojectenv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```


Start and enable gunicorn socket

```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

Check if gunicorn socket created successfully `file /run/gunicorn.socket`

Check gunicorn socket status by `sudo systemctl status gunicorn.socket`
Check gunicorn service status by `sudo systemctl status gunicorn`

Check gunicorn socket logs by `sudo journalctl -u gunicorn.socket`
Check gunicorn servicelogs by `sudo journalctl -u gunicorn`

Trigger gunicorn service using curl by `curl --unix-socket /run/gunicorn.socket localhost`

Veer incase you wish to restart gunicorn do it by 
```
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

Basically on server reboot the socket will be created automatically by systemd
and if there is an incoming request then systemd will launch the gunicorn service ;)

