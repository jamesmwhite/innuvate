import os
import sys

path = '/srv/www'
if path not in sys.path:
    sys.path.insert(0, '/srv/www')
sys.path.insert(0, '/srv/www/innuvate/ideas')
sys.path.insert(0, '/srv/www/innuvate')

os.environ['DJANGO_SETTINGS_MODULE'] = 'innuvate.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

