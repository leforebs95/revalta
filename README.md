# nivalta
The main application repository

## Building
Currently we utilize docker-compose locally in order to build our application.
Our containers depend on networks in order to communicate with one another. In order to build the application, first we create the necessary networks with:
```docker network create ocr-service_ocr-network authentication_auth-network file-service_file-network```
After we create our networks we can orchestrate our service containers with:
```docker compose -f docker-compose.yaml up --build --remove-orphans```
