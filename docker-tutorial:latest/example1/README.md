- See if the Docker daemon is running

	docker info

- List runnig container on this host

	docker ps

- Run Hello World example

	docker run hello-world

- List ALL containers on this host (including already stopped ones)

	docker ps --all

- Restart a contrainer

	docker start [CID]

- Check output of a detached container

	docker logs [CID]

- Remove a contianer

	docker rm [CID]

- Pull Python image

	docekr pull python

- Run Python in interactive mode

	docker run -it python

- Run Python command in container

	docker run python python -c 'print("Hi from Python")'

- Make container remove itself after execution

	docker run --rm python python -c 'print("Hi from Python")'

- ** PRO-TIPP:Remove all stopped container at once **

	docker rm $(docker ps -aq)

- List locally stored images

	docker image ls

- Remove image

	docker image rm hello-world


- Pull Porrtainer image

	docker pull portainer/portainer

- Create volume for Portainer to persist data during restarts
	
	docker volume create portainer_data

- Start Portainer detached

	docker run -d -p 9000:9000 -p 8000:8000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer

 Visit <http://localhost:9000> to start Portainer


