
# Commands
1. docker network create twitternet
2. docker-compose up -d --build
3. docker stop $(docker ps -a -q)
4. docker rm $(docker ps -a -q)

# clean up space
docker system prune
