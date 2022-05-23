FROM node:latest
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
COPY ./flag.txt /flag.txt
CMD ["node","index.js"]