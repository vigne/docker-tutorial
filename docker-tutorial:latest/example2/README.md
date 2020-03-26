# Building a Container and Define a Service Stack

## Idea

In `scr` is the source code of a simple Pyhton Flask application, which does nothing more than responding a string with the number of visits when requested via HTTP. If a host named `redis` is found hosting a Redis database, it will use it to store the numnber of visits.

## Usage

### Dockerfile

Use `docker build -t our_flask_app .` to build an image with your application.
If successful, use `docker run -e NAME Rick -p 5000:5000 our_flask_app` to start it.

Visit <http://localhost:5000> *(Visists are not counted due to the lack of a Redis service running)*

### docker-compose

The `docker-compose` file defines two services, one of which is based on the `our_flask_app` image we built before, and the other is a Redis database. Note that the name of the service is `redis` and both services are attached to same network. This allows our application to count how of the resource was requested.

