# specify the image you want to use build docker image

FROM python:3.9

# Maintainer name to let people know who made this image.

MAINTAINER Kartik <kartik@gmail.com>

#apt is the ubuntu command line tool for advanced packaging tool(APT) for sw upgrade '''

RUN apt update && \
    apt install -y netcat-openbsd

# set the env variable to tell where the app will be installed inside the docker

ENV INSTALL_PATH /Docker-Flask
RUN mkdir -p $INSTALL_PATH

#this sets the context of where commands will be ran in and is documented

WORKDIR $INSTALL_PATH

# WORKDIR /home/app

# COPY ./run.py/ ./home/app/
# COPY ./app/ ./home/app/

# Copy in the application code from your work station at the current directory
# over to the working directory.

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /Docker-Flask/docker-entrypoint.sh

CMD ["/bin/bash", "/Docker-Flask/docker-entrypoint.sh"]
