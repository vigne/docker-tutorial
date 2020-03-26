eval $(docker-machine env imse1)
docker-compose -f docker-compose.prod.yaml build
docker stack deploy -c docker-compose.prod.yaml imse-example

echo " ==> Visit: http://localhost:8080"
