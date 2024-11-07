<h1 align="center" style="font-size: 30px">Clean Architecture user system</h1>

<p align="center">
    <a href="https://docs.python.org/3.10/">
        <img src="https://img.shields.io/badge/Python-%20v3.11-blue.svg"/>
    </a>
    <img src="https://img.shields.io/badge/Coverage-100%25-grren.svg"/>
    <a href="./LICENSE.md">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg"/>
    </a>
    <a href="https://black.readthedocs.io/en/stable/">
        <img src="https://img.shields.io/badge/Code%20style-black-000000.svg"/>
    </a>
</p>

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

## To run in production mode

Provide a `SECRET_KEY` environment var and then, using [docker-compose](https://docs.docker.com/compose/), run the app

```bash
export SECRET_KEY=your_key
docker compose up --build
```

It'll create two containers: `frigatto_app` for the REST API and `frigatto_mongodb` for the database.

After that, the api will be visible at `http://localhost:8000` and the OpenAPI docs at `http://localhost:8000/docs`.

## To run in test mode

Use [docker-compose](https://docs.docker.com/compose/) to run the app

```bash
docker compose -f compose.tests.yml up --build
```

It'll create two containers: `frigatto_app_test` for the REST API and `frigatto_mongodb_test` for the database.

After that, the unit tests will be executed, and if all they pass, the api will be visible at `http://localhost:8001` and the OpenAPI docs at `http://localhost:8001/docs`.

> ⚠️ The data won't be persisted in test mode. They're deleted on each start in test mode.

<br/>

# License

[MIT](./LICENSE.md) - Alberto Frigatto, 2024
