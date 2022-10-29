
import os, sys
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
# sys.path.append('/root/miniconda3/lib/python3.9/site-packages/')
# sys.path.append('/usr/lib/python3.6/site-packages/')
# sys.path.append('/root/emotion-backend/')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emotion.settings')