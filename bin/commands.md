### Nginx

Check nginx config syntax:
`sudo nginx -t`

Reload nginx after changing config:
`sudo nginx -s reload`

### Gunicorn

Run it directly in the shell:
`gunicorn main.wsgi:application --workers 3 -b 0.0.0.0:8000 --log-level DEBUG`

### Daphne

Run daphne (asgi server for websockets) in shell like this:
`daphne -u /tmp/daphne.sock main.asgi:application`

### Sockets

List all unix sockets on local machine

Linux:
`netstat -a -p --unix`

Mac:
`netstat -a -f unix`

### Add domain to IP address

In `/etc/hosts` file append like this:

```
127.0.0.1 educaproject.com www.educaproject.com

127.0.0.1 mydomain.com www.mydomain.com
```

Veer you can add as many domains like this but this
is just to test locally.
Also all these domains must be added to Django's `Allowed Hosts` settings.

### SSL Certificate

We can generate a self signed SSL/TLS certificate from the command line for nginx while
testing. In this case, we are generating a private key and a 2048-bit SSL/TLS certificate that is valid for
one year.

We will be asked some info about the project. The most important option is `Common Name`
where we specify the `domain` name for the project.

This will generate inside the `ssl/` directory an `educa.key` private key and an `educa.crt`
file which is that actual certificate

```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ssl/educa.key -out ssl/educa.crt
```
