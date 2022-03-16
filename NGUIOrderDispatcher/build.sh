GIT_SSH_COMMAND='ssh -i /home/ubuntu/.ssh/id_rsa_orders_chifuri -o IdentitiesOnly=yes' git pull

docker-compose up -d --build
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py collectstatic --no-input --clear
docker-compose restart nginx  # Sometimes the connection between nginx and web fails