# This Dockerfile builds the React client and API together
#
# docker build -f Dockerfile -t react-flask-app .
#
# docker run --rm -p 3000:3000 react-flask-app
#

# Build step #1: build the React front end
FROM node:16-alpine as build-step
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH

COPY ./frontend/package.json ./
COPY ./frontend/index.html ./
COPY ./frontend/src ./src
COPY ./frontend/public ./public

RUN npm install
RUN npm run build

# Build step #2: build the API with the client as static files
FROM python:3.10-alpine
WORKDIR /app
COPY --from=build-step /app/dist ./build

RUN mkdir ./api
COPY ./backend/requirements.txt ./backend/api.py ./backend/.flaskenv ./api/
COPY ./backend/instance/app.sqlite3 ./api/instance/
RUN pip install -r ./api/requirements.txt
ENV FLASK_DEBUG 1

EXPOSE 3000
WORKDIR /app/api
CMD ["gunicorn", "-b", ":3000", "api:app"]