#source https://vuejs.org/v2/cookbook/dockerize-vuejs-app.html

FROM node:10.16.0-alpine as build-stage

WORKDIR /app
COPY package*.json ./

RUN npm install
COPY . .
RUN npm run build

EXPOSE 8080
CMD ["npm", "run", "serve"]

FROM nginx:1.16.1-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80
CMD [ "nginx", "-g", "daemon off;"]
