FROM debian:latest
MAINTAINER Will Murnane "will.murnane@gmail.com"

# keep upstart quiet
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -sf /bin/true /sbin/initctl

# no tty
ENV DEBIAN_FRONTEND noninteractive

# get up to date
RUN apt-get update --fix-missing && apt-get -y install \
  build-essential \
  git \
  libpq-dev \
  python3 \
  python3-dev \
  python3-pip \
  python3-psycopg2 \
  python3-setuptools \
  python3-virtualenv \
  virtualenv

# create a virtual environment and install all depsendecies from pypi
RUN virtualenv --python=python3 /opt/venv
ADD ./requirements.txt /opt/venv/requirements.txt
RUN /opt/venv/bin/pip3 install -r /opt/venv/requirements.txt

# file management, everything after an ADD is uncached, so we do it as late as
# possible in the process.

RUN git clone https://github.com/willmurnane/Magstock-food-calculations.git /opt/app
WORKDIR /opt/app
RUN echo 201506092039
RUN /opt/venv/bin/python3 manage.py makemigrations
RUN /opt/venv/bin/python3 manage.py migrate
RUN /opt/venv/bin/python3 manage.py loaddata users events meals prices units mealcomponent mealsinevent
RUN chown -R www-data /opt/app

CMD /opt/venv/bin/gunicorn foodcalc.wsgi -w 4 -b 0.0.0.0:5000 --log-level=debug --chdir=/opt/app --access-logfile /sharedlogs/gunicorn-access.log --error-logfile /sharedlogs/gunicorn-error.log

# expose port(s)
EXPOSE 5000
