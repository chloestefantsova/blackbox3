# BlackBox3

This is a system for hosting task-based CTFs. It was first used for hosting School CTF by SiBears team in 2015 (http://school-ctf.org/) and is currently in clean-up mode.

## Installation Instructions

This section describes the process of deploying BlackBox3 for devlopment purposes. The production setup steps are to be written later. The instructions given here are tested on Ubuntu 14.04. You may need to adjust them for your OS.

### Step 1. Install Required Ubuntu Packages

* python2.7
* python-pip
* git
* redis-server
* postgresql
* libpq-dev

TODO: complete the list of packages, including all the libraries.

You may use this command to install the packages:

```bash
$ sudo apt-get install python2.7 python-pip git redis-server postgresql libpq-dev ...
```

Optionally you may install these packages that are extremely useful for debugging and maintenance:

* redis-tools

TODO: add more packages here.

### Step 2. Clone BlackBox3 Repository

You need to obtain the latest code from the project repository:

```bash
$ git clone https://github.com/stefantsov/blackbox3.git
$ cd blackbox3
```

### Step 3. Install Python Packages

The recommended way to install the required python packages is using *virtualenv* utility that itself may be installed globally using *pip* package manager:

```bash
$ sudo pip install virtualenv
```

Now, create the virtual environment and install the packages:

```bash
$ virtualenv ../bb3-env
$ source ../bb3-env/bin/activate
(bb3-env)$ pip install -r requirements.txt
```

### Step 4. Install NodeJS Utilities

BlackBox3 uses some utilities from NodeJS, for example *less* and *yuglify*. One of the ways of obtaining those is described here.

First, download the archive that matches your OS from [this](https://nodejs.org/en/download/) page. Let's assume it is `node-v4.1.2-linux-x64.tar.gz`. Unpack the archive, and copy its contents to the virtual environment folder.

```bash
(bb3-env)$ wget -P /tmp/ https://nodejs.org/dist/v4.1.2/node-v4.1.2-linux-x64.tar.gz
(bb3-env)$ tar xvzf /tmp/node-v4.1.2-linux-x64.tar.gz -C /tmp
(bb3-env)$ rsync -a /tmp/node-v4.1.2-linux-x64/* ../bb3-env
```

You may check if these steps were successful by issuing the following command:

```bash
(bb3-env)$ which npm
```

It should print out the full path to the npm utility.

Now that the npm installation utility for NodeJS packages is available to you, install *less* and *yuglify*.

```bash
(bb3-env)$ npm install -g less yuglify
```

### Step 5. Create Local Settings File

BlackBox3 uses multiple-file settings setup. The core settings are in `settings/base.py` file, and you aren't supposed to make changes there. Everything specific to your installation should go to `settings/local.py` file. To create one you may start with copying `settings/local_example.py` file to `settings/local.py` and making changes there.

```bash
(bb3-env)$ cp settings/local_example.py settings/local.py
(bb3-env)$ vim settings/local.py
```

Basically, you want to change the following:

* `SECRET_KEY` to any random string,
* entries in `DATABASES` dictionary (see further the instructions on database setup),
* `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and `EMAIL_USE_TLS` if you plan to send emails, or `EMAIL_BACKEND` if you want to change the mailing behavior,
* uncomment `WSGI_APPLICATION` for development purposes.

### Step 6. Setup Database

If you have the PostgreSQL package installed, you may use the following to create the database user and the database for your BlackBox3 installation.

```bash
(bb3-env)$ sudo su - postgres
$ createuser -D -E -R -P -S blackbox3 # it will ask for a password
$ createdb -E utf8 -O blackbox3 blackbox3
$ exit
```

Now you can use `blackbox3` as the value for `NAME` and `USER` fields in the `DATABASES` dictionary (see Step 5) and the entered password as the value of `PASSWORD` field. You may also need to change the value of `HOST` from `127.0.0.1` to `localhost` depending on your PostgreSQL settings.

If everything was setup properly, you may now initialize the database tables:

```bash
(bb3-env)$ python manage.py migrate
```

Finally, you want at least one `Game` object in your database. Here is how you create it.

```bash
(bb3-env)$ python manage.py shell_plus
...
>>> Game.objects.create()
>>> exit()
```

### Step 7. Running BlackBox3

Everything is ready for the first launch of your BlackBox3 installation! For this you need two consoles: one is to run the Django project, and another is to run celery. Make sure your Redis is already running (it's true if you're using Ubuntu, and just installed redis-server package).

In the first console type this:

```bash
(bb3-env)$ python manage runserver
```

In the second console type this:

```bash
(bb3-env)$ celery -A slr1 worker -l info
```

If everything was ok, you may now access http://localhost:8000/ with your browser and see the brand new empty BlackBox3 page!

## Contribution

TODO: write about branching model, versioning, testing, etc.

## Contacts

Please, email d.a.stephantsov@gmail.com if you have any questions of suggestions.
