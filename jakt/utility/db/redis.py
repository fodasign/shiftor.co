# coding=utf-8
from __future__ import absolute_import
import logging
from urlparse import urlparse
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
logger = logging.getLogger(__name__)

try:
    import redis
except ImportError:
    raise ImproperlyConfigured("Redis not installed. Try `pip install redis`")

url = getattr(settings, "REDIS_URL", None)
options = getattr(settings, "REDIS_OPTIONS", {})
if not url:
    raise ImproperlyConfigured("Redis url is not set and required.")

parsed_url = urlparse(url)
db = None
try:
    db = int(url.path.replace("/", ""))
except (AttributeError, ValueError, TypeError):
    db = 0

options.setdefault("host", parsed_url.hostname)
options.setdefault("port", parsed_url.port)
options.setdefault("db", db)
options.setdefault("password", parsed_url.password)
options.setdefault("max_connections", 1000)

pool = redis.ConnectionPool(**options)

def get_connection ():
    return redis.StrictRedis(connection_pool=pool)
