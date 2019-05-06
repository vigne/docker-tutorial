# load environment settings
include .env
export

# build all images
images:
	# docker build -t imse/${MATRIKEL_NR}_example -f src/Dockerfile.example ${PROJECT_PATH}/src
	docker-compose ${COMPOSE_ARGS} build


# run example container in development mode
# allow to run current version of your code without rebuilding the container
example.dev:
	docker run \
	--rm \
	-it \
	--name ${MATRIKEL_NR}_imse_app \
	--network ${MATRIKEL_NR}_imsenet \
	-p 4000:80 \
	-v ${PROJECT_PATH}/src/example:/app/src \
	-v ${PROJECT_PATH}/src/libraries:/app/libraries \
	-e "MODE=Dev" \
	-e "NAME=${MATRIKEL_NR}" \
	imse/${MATRIKEL_NR}_example


# start all DBs and admin tools
db.up:
	docker-compose ${COMPOSE_ARGS} up --detach redis-stats redis


up:
	# update container befor starting
	docker-compose ${COMPOSE_ARGS} build
	# start all services
	docker-compose ${COMPOSE_ARGS} up --detach

# stop all DBs and admin tools
down:
	# use - to continue on error
	-docker stop ${MATRIKEL_NR}_imse_app
	docker-compose ${COMPOSE_ARGS} down


# start portainer as Docker managment tool
portainer:
	docker run \
	--detach \
	-p 9000:9000 \
	--name portainer \
	-v /var/run/docker.sock:/var/run/docker.sock \
	-v portainer_data:/data \
	portainer/portainer
