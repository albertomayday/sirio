# TPV Verifactu (Beta)

Sistema punto de venta táctil para hostelería con cumplimiento automático VERI*FACTU al estar conectado a Internet.

## Requisitos

- Docker
- Docker Compose

## Instalación

### Requisito Indispensable: Dongle de Seguridad
Este software requiere un dongle de seguridad USB conectado al servidor para funcionar. Sin este dispositivo, el sistema no iniciará.

### Pasos de Instalación

1. Conectar el Dongle de Seguridad USB al servidor.
2. Ejecutar el asistente de instalación:
   ```bash
   python3 install_with_dongle.py
   ```
   Este asistente verificará la presencia del dongle y generará/validará la licencia necesaria.
3. Una vez completada la verificación, ejecutar `docker-compose up --build` para iniciar los servicios.

## Estructura del Proyecto

- `backend/`: Código fuente del backend (FastAPI).
- `frontend/`: Código fuente del frontend (React).
- `licensing/`: Scripts y claves para el sistema de licenciamiento.

## Uso

- Acceder al frontend en `http://localhost:80`.
- Acceder a la documentación de la API en `http://localhost:8000/docs`.

## Licencia

Este proyecto está protegido por derechos de autor.
