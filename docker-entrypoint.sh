#! /bin/bash
echo "start the migration."

python manage.py makemigrations --noinput
python manage.py migrate  --noinput

echo "blog data migration completed."

echo "start initialization data."
python manage.py loaddata categories.json
echo "blog data initialization completed."