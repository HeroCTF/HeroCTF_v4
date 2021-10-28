FROM node:16
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install 
# If for production
# RUN npm ci --only=production

# Bundle app source
COPY . .

#Ca c'est pour les ports tsé
EXPOSE 4300

CMD [ "node", "index.js" ]