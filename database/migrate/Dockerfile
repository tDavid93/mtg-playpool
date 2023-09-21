FROM ubuntu:22.04
RUN apt-get update && apt-get install -y wget pgloader sqlite3
RUN wget https://mtgjson.com/api/v5/AllPrintings.sqlite
ENTRYPOINT pgloader sqlite:///AllPrintings.sqlite postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@database:5432/$POSTGRES_DB




