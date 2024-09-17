# Shape and Plate

Shape and Plate es una aplicación web progresiva (PWA) que utiliza inteligencia artificial para generar rutinas de ejercicio personalizadas y proporcionar recetas de comida basadas en los datos y necesidades nutricionales de cada usuario.

## Características

- Generación de rutinas de ejercicio personalizadas.
- Generación de recetas de comida basadas en los datos del usuario y las necesidades nutricionales de la rutina.
- Interfaz amigable y fácil de usar.
- Funcionalidad de PWA para instalación en dispositivos móviles.
- Modo oscuro/claro.
- Animación de carga personalizada.

## Requisitos

- Python 3.x
- Django
- MySQL
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
        DJANGO_ENV=development
        GOOGLE_API_KEY=tu_google_api_key
        GOOGLE_APPLICATION_CREDENTIALS_JSON='{
          "type": "service_account",
          "project_id": "shapeandplate",
          "private_key_id": "tu_private_key_id",
          ...
        }'
        MYSQLDATABASE=nombre_de_tu_base_de_datos
        MYSQLUSER=tu_usuario_mysql
        MYSQLPASSWORD=tu_contraseña_mysql
        MYSQLHOST=tu_host_mysql
        MYSQLPORT=tu_puerto_mysql
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

1. Inicia sesión o regístrate en la aplicación.
2. Ve a la sección "Workout".
3. Completa el formulario con tus datos personales (edad, altura, peso, ejercicio semanal, tipo de dieta).
4. Haz clic en "Generar Rutina" para obtener una rutina de ejercicio personalizada.

### Generar Recetas de Comida

1. Después de generar tu rutina de ejercicio, ve a la sección "Plate".
2. La aplicación te proporcionará recetas de comida basadas en tus datos y las necesidades nutricionales de la rutina.
3. Revisa las recetas y sigue las instrucciones para preparar tus comidas.

## Características Adicionales

- Modo oscuro/claro: Puedes cambiar entre el modo oscuro y claro usando el botón en la barra de navegación.
- PWA: La aplicación puede ser instalada como una PWA en dispositivos móviles para un acceso más rápido y una experiencia similar a una aplicación nativa.

## Contribuir

Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva característica'`).
4. Sube tus cambios a tu fork (`git push origin feature/nueva-caracteristica`).
5. Abre un Pull Request en el repositorio original.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
