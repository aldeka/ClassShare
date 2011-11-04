import os
import site
import sys

site.addsitedir('/groups/classshare/env/class_env/lib/python2.7/site-packages')

sys.path.append('/groups/classshare')
sys.path.append('/groups/classshare/classshare')
os.environ['DJANGO_SETTINGS_MODULE'] = 'classshare.live_settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
