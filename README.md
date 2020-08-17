# rasachatbot

This is a complete chatbot backend built with Rasa

## Run on local machine

#### Using docker

Both action server and rasa-core runs as separate processes in the same container. Rename the .env-sample to .env and optionally update the API_KEYs, TOKENs etc.

```
docker build -t rasachatbot .
docker run -it --rm -p 5005:5005 --env-file $(pwd)/.env rasachatbot
```

It starts a webserver with rest api and listens for messages at localhost:5005

#### Test over REST api

```bash
curl --request POST \
  --url http://localhost:5005/webhooks/rest/webhook \
  --header 'content-type: application/json' \
  --data '{
    "sender": "default",
    "message": "Hi"
  }'
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 59
Access-Control-Allow-Origin: *

[{
  "recipient_id": "default",
  "text": "Hello There"
}]
```

## Test the bot in terminal
```bash
docker run --rm --volume $(pwd):/app --env-file $(pwd)/.env -it\
          --workdir /app rasachatbot bash ./scripts/start_shell.sh
```

## Run using docker compose

Optionally to run the actions server in separate container start the services using docker-compose. The action server runs on http://action_server:5055/webhook (docker's internal network). The rasa-core services uses the config/endpoints.local.yml to find this actions server

```
docker-compose up
```

#### Train Rasa model

The repository already contains a trained Rasa model at models directory. To retrain the model you can run:

```bash
docker run --rm --volume $(pwd):/app \
          --workdir /app rasa/rasa:1.10.10 \
          train --fixed-model-name rasa-model \
          --config config.yml
```

## Deploy to Heroku

```bash
heroku login
heroku create <appname>
heroku container:login
heroku container:push -a <appname> web
heroku container:release -a <appname> web
```

## Integration with Facebook

Rasa supports integration with multiple channels. Apart from exposing the REST api over http, we can integrate with facebook.

Go to https://developers.facebook.com and create an app. We can handle messages sent to a facebook page from our app. To do so add messenger to the facebook app and subscribe to a page. Update app secret and page token in config/credentials.yml. On the facebook app, update the webhook url to the deployed heroku app (https://<appname>.herokuapp.com/webhooks/facebook/webhook).
