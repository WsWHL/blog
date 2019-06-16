#! /bin/bash
echo "start the migration."

python manage.py makemigrations --noinput
python manage.py migrate  --noinput

echo "blog data migration completed."