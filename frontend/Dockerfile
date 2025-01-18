FROM node:slim
WORKDIR /app
COPY . .
RUN yarn
RUN yarn generate
EXPOSE 3000
CMD ["yarn", "start"]
