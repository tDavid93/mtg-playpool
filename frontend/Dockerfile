FROM node:18-alpine

WORKDIR /app
RUN npm install -g create-react-app
RUN npm install -g react-scripts


COPY mtg-playpool-frontend/package.json .
COPY mtg-playpool-frontend/package-lock.json .
RUN npm install

ENTRYPOINT npm start
