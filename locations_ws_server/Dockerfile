# FROM node:10-alpine3.9
FROM node:lts-alpine

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .
