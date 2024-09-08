# Shape and Plate

Shape and Plate es una aplicación web que te ayuda a generar rutinas de ejercicio personalizadas y te proporciona recetas de comida basadas en tus datos y necesidades nutricionales. Utiliza inteligencia artificial para crear planes de ejercicio y alimentación adaptados a cada usuario.

## Características

- Generación de rutinas de ejercicio personalizadas.
- Generación de recetas de comida basadas en los datos del usuario y las necesidades nutricionales de la rutina.
- Interfaz amigable y fácil de usar.

## Requisitos

- Python 3.x
- Django
- Google Cloud SDK (para BigQuery y otras funcionalidades de Google)

## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/TomGGB/shapeandplate
    cd shapeandplate
    ```

2. Crea y activa un entorno virtual:
    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

4. Configura las variables de entorno:
    - Crea un archivo `.env` en el directorio raíz del proyecto y añade las siguientes variables:
        ```
        GOOGLE_API_KEY=tu_google_api_key
        GOOGLE_APPLICATION_CREDENTIALS_JSON='{
          "type": "service_account",
          "project_id": "shapeandplate",
          "private_key_id": "tu_private_key_id",
          ...
        }'
        ```

5. Realiza las migraciones de la base de datos:
    ```sh
    python manage.py migrate
    ```

6. Recolecta los archivos estáticos:
    ```sh
    python manage.py collectstatic
    ```

## Ejecución

1. Inicia el servidor de desarrollo de Django:
    ```sh
    python manage.py runserver
    ```

2. Abre tu navegador web y ve a `http://localhost:8000` para acceder a la aplicación.

## Uso

### Generar Rutina de Ejercicio

1. Ve a la página principal de la aplicación.
2. Completa el formulario con tus datos personales (edad, altura, peso, ejercicio semanal, tipo de dieta).
3. Haz clic en "Generar Rutina" para obtener una rutina de ejercicio personalizada.

### Generar Recetas de Comida

1. Después de generar tu rutina de ejercicio, la aplicación te proporcionará recetas de comida basadas en tus datos y las necesidades nutricionales de la rutina.
2. Revisa las recetas y sigue las instrucciones para preparar tus comidas.

## Contribuir

Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva característica'`).
4. Sube tus cambios a tu fork (`git push origin feature/nueva-caracteristica`).
5. Abre un Pull Request en el repositorio original.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
