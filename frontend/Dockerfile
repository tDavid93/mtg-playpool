FROM node:18-alpine

WORKDIR /app
RUN npm install -g create-react-app

COPY mtg-playpool-frontend/package.json .
RUN npm install

ENTRYPOINT npm start
