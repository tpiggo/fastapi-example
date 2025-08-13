# start the server with postgres
docker run --name postgres -p 5433:5432 -h "127.0.0.1" -e "POSTGRES_USER=postgres" -e "POSTGRES_PASSWORD=secret" -v "/home/tpiggo/postgres_data:/var/lib/postgresql/data" -d postgres:latest
