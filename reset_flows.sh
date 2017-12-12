rm demo/example/migrations/0001_initial.py
rm db.sqlite3

./manage.py makemigrations
./manage.py migrate

python add_fixtures.py
