import os
import subprocess
from time import sleep
import signal


os.system("cd D:\db-project && php artisan serve")
# child = subprocess.Popen("exec cd D:\db-project && php artisan serve", stdout=subprocess.PIPE, shell=True)
c = 0
while True:
    c+=1
    sleep(3)
    print("ok")
    if c == 3:
        break

# child.kill()
# os.system("php artisan serve")