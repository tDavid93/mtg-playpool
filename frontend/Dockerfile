FROM node:18-alpine

WORKDIR /app

COPY mtg-playpool-frontend/package.json .
RUN npm install

ENTRYPOINT npm start
