FROM node:16-alpine as build-step

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY . ./

RUN yarn install


CMD ["yarn", "start"]
