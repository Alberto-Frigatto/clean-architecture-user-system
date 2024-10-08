<h1 align="center" style="font-size: 30px">Clean Architecture user system</h1>

<p align="center">
    A Python user management REST API built following <b>Clean Architecture</b> principles. The project adheres to best practices such as <b>TDD</b>, <b>SOLID</b>, and <b>Dependency Injection</b>, ensuring maintainability, scalability, and a clean, modular design.
</p>

<br/>

# Table of contents

- [Installation](#installation)
- [License](#license)

<br/>

# Installation

Clone this repository

```bash
git clone https://github.com/Alberto-Frigatto/clean-architecture-user-system.git
```

Go to repository where you've cloned it

```bash
cd path/to/repository/clean-architecture-user-system
```

Provide a `SECRET_KEY` environment var and then, using [docker-compose](https://docs.docker.com/compose/), run the app

```bash
export SECRET_KEY=your_key
docker-compose up
```

It'll create two containers: `frigatto_app` for the REST API and `mongodb` for the database.

After that, the api will be visible at `http://localhost:8000` and the OpenAPI docs at `http://localhost:8000/docs`.

<br/>

# License

[MIT](./LICENSE.md) - Alberto Frigatto, 2024
