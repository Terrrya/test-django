# Hacker news proxy
<hr>

This proxy server opens Hacker News site and changes words with 6 letters by adding "™" to them. You can feel free 
to browse the site. Only words have been changed, all other functionality will work as original.

## Installing using GitHub
<hr>

### Run with python

Python3 should be installed

```python
git clone https://github.com/Terrrya/test-django
cd test-django
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8232
```

### Run with docker
<hr>

Docker should be installed

```python
git clone https://github.com/Terrrya/test-django
cd test-django
docker build -t hackernewsproxy .
docker run -p 8232:8232 hackernewsproxy
```

### Using
Now you can run in your browser 127.0.0.1:8232 and use it.