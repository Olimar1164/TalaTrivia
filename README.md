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
    ```json
    {
        "refresh": "your_refresh_token"
    }
    ```
    
### Usuarios

- **Crear usuario**: `POST /api/users/`
    ```json
    {
        "username": "newuser",
        "email": "newuser@example.com",
        "name": "New User",
        "password": "password",
        "role": "player"
    }
- **Listar usuarios**: `GET /api/users/`
    ```json
    [
        {
            "id": "uuid",
            "username": "admin",
            "email": "admin@example.com",
            "name": "Admin User"
        },
        {
            "id": "uuid",
            "username": "newuser",
            "email": "newuser@example.com",
            "name": "New User"
        }
    ]
    ```

### Preguntas

- **Crear pregunta**: `POST /api/questions/`
    ```json
    {
        "question_text": "What is the capital of France?",
        "difficulty": "easy",
        "options": [
            {"option_text": "Paris", "is_correct": true},
            {"option_text": "London", "is_correct": false},
            {"option_text": "Berlin", "is_correct": false},
            {"option_text": "Madrid", "is_correct": false}
        ]
    }
    ```

- **Listar preguntas**: `GET /api/questions/`
    ```json
    [
        {
            "id": 1,
            "question_text": "What is the capital of France?",
            "options": [
                {"id": 1, "option_text": "Paris", "is_correct": true},
                {"id": 2, "option_text": "London", "is_correct": false},
                {"id": 3, "option_text": "Berlin", "is_correct": false},
                {"id": 4, "option_text": "Madrid", "is_correct": false}
            ]
        }
    ]
    ```

### Trivias

- **Crear trivia**: `POST /api/trivias/`
    ```json
    {
        "name": "Trivia 1",
        "description": "Description for Trivia 1",
        "questions": [
            {"id": 1},
            {"id": 2},
            {"id": 3}
        ]
    }
    ```

- **Listar trivias**: `GET /api/trivias/`
    ```json
    [
        {
            "id": 1,
            "name": "Trivia 1",
            "description": "Description for Trivia 1",
            "questions": [
                {"id": 1, "question_text": "What is the capital of France?", "options": [...]},
                {"id": 2, "question_text": "What is 2 + 2?", "options": [...]},
                {"id": 3, "question_text": "What is the color of the sky?", "options": [...]}
            ]
        }
    ]
    ```

### Participación en Trivias

- **Ver trivias asignadas**: `GET /api/participations/`
    ```json
    [
        {
            "id": 1,
            "user": "uuid",
            "trivia": "uuid",
            "trivia_name": "Trivia 1",
            "score": 10,
            "completed": false
        }
    ]
    ```

- **Responder preguntas**: `POST /api/answers/`
    ```json
    {
        "question": 1,
        "selected_option": 1
    }
    ```

- **Ver puntaje y estado de participación**: `GET /api/participations/<int:pk>/`
    ```json
    {
        "id": 1,
        "user": "uuid",
        "trivia": "uuid",
        "trivia_name": "Trivia 1",
        "score": 10,
        "completed": false
    }
    ```

### Ranking de Usuarios

- **Generar ranking**: `GET /api/rankings/`
    ```json
    [
        {
            "user": "admin",
            "total_score": 30,
            "trivias": [
                {"trivia_name": "Trivia 1", "score": 10},
                {"trivia_name": "Trivia 2", "score": 20}
            ]
        },
        {
            "user": "newuser",
            "total_score": 20,
            "trivias": [
                {"trivia_name": "Trivia 1", "score": 20}
            ]
        }
    ]
    ```

- **Generar ranking por trivia**: `GET /api/rankings/<int:trivia_id>/`
    ```json
    [
        {
            "user": "admin",
            "total_score": 10,
            "trivias": [
                {"trivia_name": "Trivia 1", "score": 10}
            ]
        },
        {
            "user": "newuser",
            "total_score": 20,
            "trivias": [
                {"trivia_name": "Trivia 1", "score": 20}
            ]
        }
    ]
    ```

- **Generar ranking por trivia y usuario**: `GET /api/rankings/<int:trivia_id>/<uuid:user_id>/`
    ```json
    {
        "user": "newuser",
        "total_score": 20,
        "trivias": [
            {"trivia_name": "Trivia 1", "score": 20}
        ]
    }
    ```

- **Generar ranking por usuario**: `GET /api/rankings/user/<uuid:user_id>/`
    ```json
    {
        "user": "newuser",
        "total_score": 20,
        "trivias": [
            {"trivia_name": "Trivia 1", "score": 20}
        ]
    }
    ```

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