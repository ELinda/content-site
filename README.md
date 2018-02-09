# content-site

```
git clone git@github.com:ELinda/content-site.git
git checkout develop

cd content-site
alias python=python3
alias pip=pip3
python -m venv --without-pip ~/site/
source ~/site/bin/activate
sudo pip install -U -r requirements.txt
wget https://code.jquery.com/jquery-3.1.1.min.js -P static/

```

## WSGI

To kill WSGI processes:
```
ps aux | grep WSG | grep -v grep | cut -f 2 -d " "| xargs -I pid sudo kill -s QUIT
```

The log directory of app.yaml may need to be edited, or created, if it doesn't exist.
To run WSGI as a daemon:
```
uwsgi --yaml app.yaml
```

To run WSGI (press Ctrl+C to stop):
```
uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:application
```

WSGI must be restarted for the site to reflect any changes in application or template files. 


## NGINX

Edit the location block of `/etc/nginx/nginx.conf`, to point to the original flask port (who's defaulted to 5000):
```
...
location / {
    include uwsgi_params;
    uwsgi_pass 127.0.0.1:5000;
}
...
```

Run NGINX:
```
sudo service nginx run
```

Now your site will be accessible from port 80.

