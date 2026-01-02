FROM node AS install

RUN groupadd --gid 12345 app
RUN useradd --uid 12345 --gid app --shell /bin/bash --create-home app

WORKDIR /tmp/build_app

COPY package.json index.js /tmp/build_app/

RUN apt-get update && apt-get install -y curl
RUN npm install
RUN mkdir -p /usr/src/myapp && \
    mv /tmp/build_app/index.js  /usr/src/myapp && \
    mv /tmp/build_app/node_modules /usr/src/myapp/ && \
    chown -R app:app /usr/src

FROM node

RUN groupadd --gid 12345 app && \
  useradd --uid 12345 --gid app --shell /bin/bash --create-home app

COPY --from=install --chown=app:app /usr/src /usr/src

WORKDIR /usr/src/myapp

USER app
EXPOSE 8080

CMD ["node", "index.js"]
