# TalaTrivia 🎉

¡Bienvenid@ a TalaTrivia! Este proyecto es parte de un desafío para TALANA, consta de la construcción de una API que gestione un juego de trivia. Los usuarios pueden participar en trivias, responder preguntas y competir por obtener el mayor puntaje posible.

## Características 🚀

- **Usuarios**: Crear y listar usuarios con roles de administrador y jugador.
- **Preguntas**: Crear y listar preguntas con opciones de respuesta y niveles de dificultad.
- **Trivias**: Crear trivias, asignar preguntas y usuarios.
- **Participación en Trivias**: Los usuarios pueden ver y responder trivias asignadas a ellos.
- **Ranking de Usuarios**: Generar un ranking de usuarios basado en sus puntajes en una trivia específica.

## Requisitos 📋

- Docker
- Docker Compose

## Configuración 🛠️

1. Clona el repositorio:
    ```sh
    git clone https://github.com/Olimar1164/TalaTrivia.git
    cd talatrivia
    ```

2. Crea o mueve el archivo `.env` en la raíz del proyecto con las variables de entorno
    (se envía por correo)

3. Construye y levanta los contenedores Docker:
    ```sh
    docker-compose up --build
    ```
    este paso tarda mas de lo habitual, ya que migra la base de datos postgres
    con datos ficticios(siento no poder agregar preguntas mas ad-hoc a recursos humanos).

4. Accede a la aplicación en tu navegador:
    ```
    http://localhost:8000
    ```

## Endpoints de la API 📡

### Autenticación

- **Obtener token JWT**: `POST /api/token/`
    ```json
    {
        "username": "admin",
        "password": "adminpassword"
    }
    ```

- **Refrescar token JWT**: `POST /api/token/refresh/`

### Usuarios

- **Crear usuario**: `POST /api/users/`
- **Listar usuarios**: `GET /api/users/`

### Preguntas

- **Crear pregunta**: `POST /api/questions/`
- **Listar preguntas**: `GET /api/questions/`

### Trivias

- **Crear trivia**: `POST /api/trivias/`
- **Listar trivias**: `GET /api/trivias/`

### Participación en Trivias

- **Ver trivias asignadas**: `GET /api/participations/`
- **Responder preguntas**: `POST /api/answers/`
- **Ver puntaje y estado de participación**: `GET /api/participations/<int:pk>/`

### Ranking de Usuarios

- **Generar ranking**: `GET /api/rankings/`
- **Generar ranking por trivia**: `GET /api/rankings/<int:trivia_id>/`
- **Generar ranking por trivia y usuario**: `GET /api/rankings/<int:trivia_id>/<uuid:user_id>/`
- **Generar ranking por usuario**: `GET /api/rankings/user/<uuid:user_id>/`

## TO DO 📝

- [ ] Implementar preguntas relacionadas a Recursos Humanos.
- [ ] Implementar la funcionalidad de edición y eliminación de usuarios, preguntas y trivias.
- [ ] Mejorar la validación de datos en los serializadores.
- [ ] Añadir más pruebas unitarias y de integración.
- [ ] Implementar la paginación en los endpoints de listado y estandarizar las respuestas.
- [ ] Mejorar la documentación de la API utilizando Swagger o ReDoc(cuando lo implementaba me botaba la app).

## Contribuciones 🤝

¡Las contribuciones son bienvenidas! Si tienes alguna idea o mejora, no dudes en abrir un issue o enviar un pull request.


---

¡Gracias por ver mi proyecto! 🎉