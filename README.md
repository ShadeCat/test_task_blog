Запуск

Подготовить posgress:

CREATE DATABASE testblog; CREATE USER testblog;
ALTER USER testblog PASSWORD 'testblog';
GRANT ALL ON DATABASE testblog TO testblog;

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata users
python manage.py loaddata posts

тестовые пользователи:
Doc
Bashful
Sneezy
Happy 
Dopey
Sleepy
Grumpy

Пароль у всех один:
pass
