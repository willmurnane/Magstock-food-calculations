FROM debian:latest
MAINTAINER Will Murnane "will.murnane@gmail.com"

# keep upstart quiet
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -sf /bin/true /sbin/initctl

# no tty
ENV DEBIAN_FRONTEND noninteractive

# get up to date
RUN apt-get update --fix-missing

# global installs [applies to all envs!]
RUN apt-get install -y build-essential git
RUN apt-get install -y python3 python3-dev python3-setuptools
RUN apt-get install -y python3-pip python3-virtualenv virtualenv
RUN apt-get install -y nginx supervisor
RUN apt-get install -y vim strace net-tools

# stop supervisor service as we'll run it manually
RUN service supervisor stop

# build dependencies for postgres and image bindings
RUN apt-get install -y python3-psycopg2 libpq-dev

# create a virtual environment and install all depsendecies from pypi
RUN virtualenv --python=python3 /opt/venv
ADD ./requirements.txt /opt/venv/requirements.txt
RUN /opt/venv/bin/pip3 install -r /opt/venv/requirements.txt

# file management, everything after an ADD is uncached, so we do it as late as
# possible in the process.
ADD ./supervisord.conf /etc/supervisord.conf
ADD ./nginx.conf /etc/nginx/nginx.conf

RUN git clone https://github.com/willmurnane/Magstock-food-calculations.git /opt/app
WORKDIR /opt/app
RUN /opt/venv/bin/python3 manage.py makemigrations
RUN /opt/venv/bin/python3 manage.py migrate
RUN /opt/venv/bin/python3 manage.py loaddata users events meals prices units mealcomponent mealsinevent
# restart nginx to load the config
RUN service nginx stop
RUN mkdir /var/log/gunicorn
RUN chown -R www-data /opt/app
RUN chown -R www-data /var/log/gunicorn

# start supervisor to run our wsgi server
CMD supervisord -c /etc/supervisord.conf -n

# expose port(s)
EXPOSE 80
