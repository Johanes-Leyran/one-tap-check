## How to set-up

Make a virtual environment, then install the requirements.

Navigate through the project to find manage.py then run this command.

```
manage.py makemigrations
```
And then

```
manage.py migrate
```

This will make the tables needed in the database and apply it.

After running `makemigrations` and `migrate`.

```
manage.py runserver
```

This will run the app and you are ready to go.

This project is built to run with [RFID hardware](https://github.com/Johanes-Leyran/one-tap-check-hardware).
