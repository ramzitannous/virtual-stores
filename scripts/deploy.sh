docker-compose pull backend && \
docker-compose up -d db redis
docker-compose -p backend up -d  --force-recreate backend beat worker flower