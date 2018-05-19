
import sys,os
from django.core.wsgi import get_wsgi_application

sys.path.insert(0,'D:\git仓库\GridForecastSys')

# sys.path.extend(['Path_to_your_django_project',])
os.environ.setdefault("DJANGO_SETTINGS_MODULE","GridForecastSys.settings")
# application = get_wsgi_application()

