# Imagen base con Java 11
FROM openjdk:11-jdk


# Copia tu instalación de Keycloak (keycloak-11.0.1) dentro del contenedor
ADD ./keycloak-11.0.1 /opt/keycloak-11.0.1

# Define el directorio de trabajo
WORKDIR /opt/keycloak-11.0.1/bin

RUN chmod +x /opt/keycloak-11.0.1/bin/standalone.sh
# Exponemos el puerto 8080 porque ese es el puerto por defecto de standalone.sh
EXPOSE 8585

# Ejecutar el mismo comando que usas localmente
CMD ["./standalone.sh", "-b", "0.0.0.0"]
