#!/bin/bash

cp db-template.db tests/resources/db-template.db
php artisan serve --env=ui.test &
./main.py -v
# jobs -l | grep "php artisan serve" | awk '{print $2}' | xargs kill -9
ps aux | grep "db-project/server.php" | head -1 | awk '{print $2}' | xargs kill -9
