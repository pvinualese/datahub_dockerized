# Lanzar entorno completo

Lo primero que hay que hacer es crear la red datahub_network:

    docker network create datahub_network

## 0 - Keycloak (opcional)

En la carpeta keycloak está el docker compose que lo despliega.

    sudo docker-compose -f docker-compose-key.yml up -d --build

Interfaz de Keycloak en http://localhost:8585

Usuario: admin

Contraseña: admin

Pasos a seguir:

- Creación de nuevo cliente datahub

- Click en el nuevo cliente

En el apartado Clients/datahub/Settings:

-- Client Protocol: openid-connect

-- Acces Type: confidential

-- Standard Flow Enabled, Direct Access Grants Enabled, Service Accounts Enabled, Authorization Enabled

-- Valid Redirect URIs: http://localhost:9002/callback/oidc, http://localhost:9003/callback/oidc, http://localhost:9004/callback/oidc, http://localhost:9005/callback/oidc


En el apartado Clients/datahub/Credentials:

-- Client Authenticator: Client Id and Secret

-- Secret -> Nos sirve para meterlo en el Docker Compose de las instancias de datahub

- Creación de nuevos usuarios

-- Asignar emails, nombre y apellidos

-- User Enabled, Email Verified

-- Credentials -> Asignar contraseña



## 1 - Lanzar servicios de DataHub origen 

Dentro de las carpetas datahub-quickstart/quickstar-clima, datahub-quickstart/quickstart-prec y datahub-quickstart/quickstart-drugs estan los docker compose que despliegan los catálogos origen. Para desplegarlos:

    sudo docker-compose -f docker-compose-quickstart-clima.yml up -d --build

    sudo docker-compose -f docker-compose-quickstart-prec.yml up -d --build

    sudo docker-compose -f docker-compose-quickstart-drugs.yml up -d --build


¡¡IMPORTANTE!!
Si no está el fichero .jar en datahub-quickstart/datahub-upgrade lanzar con Docker Desktop el entorno y descargarlo cuando se inicie el servicio datahub-upgrade

Tras la ejecución de los comandos se despliegan tres instancias diferentes de DataHub, que podemos abrir en http://localhost:9002, http://localhost:9003 y http://localhost:9005.

En estas instancias se habrán creado los dominios. tags, terms etc.
A través de las interfaces podemos obtener el token de acceso (esperar un poco a que se desplieguen todos los iconos de la barra lateral, que a veces tarda).

Si se decide implementar el servicio de keycloak hay que dejar descomentadas estas lineas en los contenedores del frontend:

    - AUTH_OIDC_ENABLED=true
    - AUTH_OIDC_CLIENT_ID=datahub
    - AUTH_OIDC_CLIENT_SECRET=8a665e67-fc6e-490f-a6e2-a96e88ab245d
    - AUTH_OIDC_DISCOVERY_URI=http://192.168.64.2:8585/auth/realms/master/.well-known/openid-configuration
    - AUTH_OIDC_BASE_URL=http://localhost:9005
    - AUTH_SESSION_TTL_HOURS=1
    - MAX_SESSION_TOKEN_AGE=1h
    - AUTH_OIDC_USER_NAME_CLAIM=email
    - AUTH_OIDC_USER_NAME_CLAIM_REGEX=^drugs@drugs\.com$$

Además, habrá que revisar que la dirección escrita en AUTH_OIDC_DISCOVERY_URI coincida con la dirección del servicio de keycloak.

## 2 - Lanzar servicios de FIWARE (NiFi + Orion)

    sudo docker-compose -f docker-compose-fiware-clima.yml up -d --build

    sudo docker-compose -f docker-compose-fiware-prec.yml up -d --build

Con estos ficheros conseguimos lanzar NiFi. Los ficheros se encuentran en el directorio principal (datahub_dockerized)

Con los servicios Mongo y Orion no debería haber problema.

El servicio draco podría dar problema si la carpeta draco/processors está vacía. Esto se soluciona accediendo via ssh a la máquina en la que se ha desplegado todo lo de YODA. Ahí habría que copiar por scp el fichero .nar, para que el Dockerfile lo pueda usar.

Una vez están ejecutándose todos los servicios hay que crear las suscripciones en los respectivos servicios de Orion. Para ello hay que ejecutar los siguientes comandos en el interior de los contenedores (fijarse en clima y prec para ejecutarlo en el contenedor correcto):

    curl -L -X POST 'http://localhost:1026/ngsi-ld/v1/subscriptions/' -H 'Content-Type: application/ld+json' --data-raw '{"description":"Notify me when WeatherObserved appears","type":"Subscription","entities":[{"type":"WeatherObserved"}],"watchedAttributes":["stationCode"],"notification":{"endpoint":{"uri":"http://draco-clima:5050/ld/notify/weatherObserved","accept":"application/json"}},"@context":["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]}'

    curl -L -X POST 'http://localhost:1026/ngsi-ld/v1/subscriptions/' -H 'Content-Type: application/ld+json' --data-raw '{"description":"Notify me when WeatherObserved appears","type":"Subscription","entities":[{"type":"WeatherObserved"}],"watchedAttributes":["stationCode"],"notification":{"endpoint":{"uri":"http://draco-prec:5050/ld/notify/weatherObserved","accept":"application/json"}},"@context":["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]}'

Para comprobar que las solicitudes se han creado correctamente ejecutar:

    curl -L -X GET 'http://localhost:1026/ngsi-ld/v1/subscriptions/'


Interfaz de Nifi en https://localhost:9090/ y https://localhost:9191/

Usuario: admin
Contraseña: password1234567890

En NiFi basta con cargar los templates que se han subido al desplegar el servicio y ejecutar los procesadores. Hay que cambiar los procesadores finales, modificando el token de autorización, añadiendo el que hayamos obtenido desde cada interfaz de DataHub.

Tras ejecutar los procesadores se comenzarán a cargar los datasets en las 2 instancias de DataHub.

## 3 - Lanzar Airflow

Dentro de la carpeta airflow se encuentra el docker-compose.

1º hay que cambiar el token de acceso en el dag publish_to_datahub


    sudo docker-compose -f docker-compose-air.yml up -d --build

Accedemos a la interfaz en http://localhost:58080

Usuario y contraseña: airflow


Al ejecutar los dags comenzará la carga en DataHub.

## 4 - Lanzar instancia federadora de DataHub

En la carpeta datahub-quickstart/quickstart-federado se encuentra el docker compose que ejecuta la instancia federadora. Con desplegar estos microservicios es suficiente, ya que la ingesta se produce en el contenedor "actions" en el momento del despliegue.

    sudo docker-compose -f docker-compose-quickstart-federado.yml up -d --build
