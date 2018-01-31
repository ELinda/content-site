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