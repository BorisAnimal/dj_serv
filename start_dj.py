import subprocess
from ip import *
import os

addr = get_ip()
port = DJ_PORT

print("HERE>>>>>>>>>>>>>>>>>>>>\n")

os.system('cmd.exe /k "myvenv\Scripts\\activate && python manage.py runserver {}:{}"'.format(addr, port))


from ipm import settings

settings.ALLOWED_HOSTS.append(addr)