# Docker Tutorial for Information Management and System Engineering

In this repository all files required for the tutorial on Docker are included.

Please note that the examples used in this material are heavily inspired
by the ones used in the official [Docker documentation](https://docs.docker.com/get-started/)


## 1. Basics

Read the slides provided on the course webpage to understand the concepts of containers and familiarize
yourself with the terminology. You may also want to recap the course slides about
this topic in CeWebs.

Multiple tools (e.g. [Portainer.io](https://www.portainer.io/)]) exist to control your docker daemon and deployments.
In this tutorial though we will stick to CLI tools, as this is common ground on every system.

### 1.1. Run "Hello World"

```
docker run \
--rm \
python:2.7-slim \
python -c 'print "Hello World from Python!"'
```

* `--rm` ... removes the container on exit
* `python:2.7-slim` ... the image used for the container
* `python -c '...'` ... the command to be executed inside the container

### 1.2. Use the interactive mode to start interpreter

```
docker run \
--rm \
--interactive \
--tty \
python:2.7-slim \
python
```

* `--interactive` ... keeps STDIN/STDOUT open
* `--tty` ... get its own terminal to avoid issues

## 2. Building an image manually

### 2.1 Create container and persist setup

#### Install dependencies

```
docker run \
--name imse_00_prep \
python:2.7-slim \
sh -c "pip install flask redis && mkdir /app"
```

* `--name imse_00_prep` ... the name of the container
* `sh -c "pip install ...` ... command to execute, i.e. install flask and redis using pip and create app folder

#### Copy source code into container

```
docker cp \
src/example \
imse_00_prep:/app/src
```

* `docker cp ...` ... copies local files into the container file system

#### Commit changes

Since you cannot change the command a container was created with, the container
needs to be persisted into a new image and restarted with a different command.

```
docker commit -m 'preped for flask' imse_00_prep imse_app:dev
docker rm imse_00_prep
```

* `docker commit` ... persists the current state of the container into a local image
* `docker rm` .... removes the stopped container after the image has been created

#### Verify container setup

To check if everything is as intended, create a new container and access it using:
```
docker run \
--rm \
--interactive \
--tty \
imse_app:dev \
bash
```

`ls /app/src` should show the `app.py` file copied earlier.

### 2.2 Mount local directories into the container at start time

During development, updating container as described above can be very cumbersome.
Thus, one can mount only the source files of your application into the
container. This way, if the code changes, the container only needs to be restarted
instead of rebuilt.

```
docker run \
--rm \
--name imse_00_dev \
--interactive \
--tty \
--publish 4000:80 \
--mount type=bind,source="$(pwd)"/src/example,target=/app/src \
--env "NAME=Developer" \
--env "MODE=Dev-Manual" \
imse_app:dev \
python /app/src/app.py
```

* `--publish 4000:80` ... exposes port 80 from the container at port 4000 on the host network, i.e. [http://localhost:4000]
* `--mount  ...` ... makes a bind mount of the local folder into the container. See [bind mounts](https://docs.docker.com/storage/bind-mounts/) for a detailed explanation.
* `python /app/src/app.py` ... the command executed on container startup

### 2.3 Create final image

When done developing, bundle everything up into one single image for later usage.

```
docker create \
--name imse_00_commit \
--publish 4000:80 \
imse_app:dev \
python /app/app.py

docker cp src/app.py imse_00_commit:/app/app.py
docker commit -m 'with app' imse_00_commit imse_app:v0.0
docker rm imse_00_commit
```

and run it like this

```
docker run \
--rm \
--name imse_00_app \
--interactive \
--tty \
--publish 4000:80 \
--env "NAME=Tired Operator" \
--env "MODE=Prod-Image" \
imse_app:v0.0 \
python /app/app.py
```

## 3. Build images using a `Dockerfile`

Using so called [Dockerfiles](https://docs.docker.com/engine/reference/builder/) all the above can be described in a single recipe.
```
# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Use pip to install dependencies
RUN pip install --trusted-host pypi.python.org redis flask

# Set the working directory to /app
WORKDIR /app

# Copy the example source directory contents into the container at /app
ADD src/example /app


# Set environment variable pointing to container-local libraries
ENV PYTHONPATH /app

# Run app.py when the container launches
CMD ["python", "app.py"]
```

**Hint:** if you see an error like this `error checking context: 'no permission to read from ` use a `.dockerignore` file
to exclude files and folder from the build context.

After a successful build, one can run the app like this:
```
docker run \
--publish 4000:80 \
--rm \
--name imse_01_app \
--env "NAME=Happy Operator" \
--env "MODE=Prod-Dockerfile" \
imse_app:latest
```

or continue using bind mounts while developing

```
docker run \
--publish 4000:80 \
--rm \
--name imse_01_app \
--env "NAME=Developer" \
--env "MODE=Dev-Dockerfile" \
--mount type=bind,source="$(pwd)"/src/example,target=/app/src \
--env "NAME=Developer" \
--env "MODE=Dev-Dockerfile" \
imse_app:dev \
python /app/src/app.py
```

## 4. Deploying a software stack using `docker-compose`

A software stack defined in a [compose file](https://docs.docker.com/compose/compose-file/) deploys several services at once. For example, an app needs an instance of Redis to connect to.

See [here for detailed discussion about compose files.

```
version: "3.2"

services:
  # your app(s)
  imse_app:
    build:
      dockerfile: Dockerfile.tutorial
      context: .
    image: imse_app:compose
    ports:
      - target: 80
        published: 4000
        protocol: tcp
    environment:
      - "MODE=Prod"
      - "NAME=Happy Composer"

  redis:
    image: redis
```

See [docker-compose.yaml]() for a more detailed example utilizing more of the
compose capabilities and acting as a blueprint for your assigments.

## 5. Hints and Tips

* Use a [`Makefile`]() to automate and **document** the usage of your services
* Expose only necessary ports on the host system
* Define common settings inside a `.env` file
