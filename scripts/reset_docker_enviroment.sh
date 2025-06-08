docker stop $(docker ps -q)
docker volume prune -f
docker rm $(docker ps -a -q)   
docker rmi $(docker images -q) 
docker-compose up -d --build --force-recreate