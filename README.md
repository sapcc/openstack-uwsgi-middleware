# openstack-uwsgi-middleware
Middleware that populates uwsgi variables with openstack request-ids and keystone informations.

### Usage
`pip install openstack-uwsgi-middleware` and add as a middleware to you paste config.

#### api-paste.ini
```ini
...
keystone = cors ... uwsgi neutronapiapp_v2_0

[filter:uwsgi]
paste.filter_factory = uwsgi_middleware:Uwsgi.factory
```
