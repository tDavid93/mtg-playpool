#!/bin/bash
docker compose down --volumes --remove-orphans
docker compose --env-file ./.env up --force-recreate --build

