#!/bin/bash
export DB_DATABASE=$(pwd)/tmp/db-template.db
export APP_ENV=ui.test

cp tests/resources/db-template.db tmp/
php artisan serve &
./main.py -v
# jobs -l | grep "php artisan serve" | awk '{print $2}' | xargs kill -9
ps aux | grep "db-project/server.php" | head -1 | awk '{print $2}' | xargs kill -9
