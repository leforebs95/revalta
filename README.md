# nivalta
The main application repository

## Building
Currently we utilize docker-compose locally in order to build our application. docker-compose will spin up three containers, `nivalta-nginx` `nivalta-svelte-server` and `nivalta-flask-server`. Up executing
```docker compose up --build --remove-orphans``` the three containers will spin up and be accesible through localhost. Note, each time you want to re-build the svelte application, it is best to rerun the compose command. Local builds are no longer needed. 
