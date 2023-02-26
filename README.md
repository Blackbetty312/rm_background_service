# rm_background_service
A simple service using python, flask and rembg in which we can remove the background from photos through the API and also gain access to photos.

## Requirements

```
docker
```

## Installation


```bash
cp .env.dev.example .env.dev
cp .env.prod.example .env.prod
cp .env.example .env
```
And change http_basic_auth_login/http_basic_auth_password for your personal values for authorization

## Build docker container

```
docker-compose build remove_background_app
```

## Run docker container in background

```
docker-compose up -d remove_background_app
```

Now you have access to application.

## Example request
You need to send POST request to /remove_background with form-data. image param need to be file with allowed extension ('jpg', 'jpeg', 'png'). Response is a file with removed background.

For get a file by filename you need to send GET request to /get_image?filename=example.png