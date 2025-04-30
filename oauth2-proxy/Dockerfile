# Imagen base mínima con Linux
FROM ubuntu:22.04

# Instalar dependencias necesarias, incluyendo ping y curl
RUN apt-get update && \
    apt-get install -y openssl iputils-ping curl && \
    apt-get clean

# Copiar la carpeta oauth2-proxy al contenedor
ADD ./oauth2-proxy-v6.1.1.linux-amd64 /opt/oauth2-proxy

# Establecer el directorio de trabajo
WORKDIR /opt/oauth2-proxy

# Exponer el puerto que usará oauth2-proxy
EXPOSE 4180


# en upstream y en oidc-issuer-url tenemos la IP de proxy_yoda y de keycloak respectivamente
# set-authorization, pass-authorization y pass-user son para que ngninx pueda leer el token y el correo del usuario
# Ejecutar el comando para iniciar oauth2-proxy
CMD ./oauth2-proxy --http-address=0.0.0.0:4180 \
  --email-domain=* \
  --cookie-secure=false \
#   --cookie-secret=$(openssl rand -base64 32 | tr -d '=+/[:space:]' | cut -c1-16) \
  --cookie-secret=1234567890123456789012 \
  --cookie-expire=5m \
  --cookie-refresh=0s \
  --upstream=http://proxy_datahub:1024 \
  --provider=oidc \
  --client-id=oauth2-proxy \
  --client-secret=834801d1-c62e-4625-9d0b-9438942834bc \
  --oidc-issuer-url="http://192.168.64.8:8585/auth/realms/master" \
  --insecure-oidc-allow-unverified-email=true \
  --redirect-url="http://localhost:4180/oauth2/callback" \
  --set-authorization-header=true \
  --pass-authorization-header=true \
  --pass-user-headers=true
