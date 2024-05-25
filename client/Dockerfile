FROM node:20.10-alpine

WORKDIR /app

RUN apk update && apk add curl

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

ENV NODE_ENV=development
ENV HOST=0.0.0.0

CMD ["npm", "run", "dev"]
