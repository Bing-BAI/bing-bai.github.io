FROM node:22-alpine
WORKDIR /app
COPY --chown=node:node server.mjs ./server.mjs
USER node
ENV PORT=9000
EXPOSE 9000
CMD ["node", "server.mjs"]
