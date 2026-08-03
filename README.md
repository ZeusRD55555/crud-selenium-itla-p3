# CRUD con Selenium - ITLA

Proyecto de **Pruebas Automatizadas con Selenium** para la aplicación web CRUD
`crud-gitflow-itla-p3`, desarrollada con Flask. Incluye un módulo de **login**
(nuevo) y una **suite completa de pruebas automatizadas** con Selenium WebDriver,
evidencias (capturas de pantalla) y reporte HTML.

## Funcionalidades

- **Autenticación**: inicio y cierre de sesión; rutas CRUD protegidas.
- **CRUD de usuarios**: crear, listar, buscar, editar y eliminar.
- **Validaciones**: nombre, correo (formato y duplicado) y teléfono.

### Credenciales de acceso

| Usuario | Contraseña |
|---------|------------|
| `admin` | `admin123` |

El usuario administrador se crea automáticamente al iniciar la aplicación.

## Tecnologías

- Python 3.14 + Flask 3.0.3 + Flask-SQLAlchemy (SQLite)
- Selenium WebDriver + webdriver-manager (Chrome)
- pytest + pytest-html
- Jira (historias de usuario) y GitHub (control de versiones)

## Estructura del proyecto

```
crud-selenium-itla-p3/
├── app/
│   ├── __init__.py          # create_app(), seed admin
│   ├── models.py            # Item, User, Admin
│   ├── routes.py            # login/logout + rutas CRUD protegidas
│   ├── templates/           # plantillas (login, CRUD, base)
│   └── static/style.css
├── tests/
│   ├── conftest.py          # fixtures y helpers de Selenium
│   ├── test_login.py
│   ├── test_crear_usuario.py
│   ├── test_listar_usuarios.py
│   ├── test_buscar_usuario.py
│   ├── test_editar_usuario.py
│   └── test_eliminar_usuario.py
├── report/report.html       # reporte HTML de las pruebas (generado)
├── screenshots/             # evidencias por escenario (generado)
├── requirements.txt
├── pytest.ini
└── run.py
```

## Instalación y ejecución

### 1. Entorno virtual y dependencias

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Iniciar la aplicación Flask

```bash
python run.py
```

La app queda disponible en `http://127.0.0.1:5000`.

### 3. Ejecutar las pruebas automatizadas

Con el servidor corriendo, en otra terminal:

```bash
.venv\Scripts\python.exe -m pytest -v
```

## Resultados

- **Reporte HTML**: `report/report.html` (se genera automáticamente).
- **Evidencias**: una captura por escenario en `screenshots/`, generada
  automáticamente al finalizar cada prueba.
- **Conteo**: 18 casos de prueba (éxito, negativo y casos límite).

## Casos de prueba

| Módulo | Casos |
|--------|-------|
| Login | correcto, incorrecto, campos vacíos |
| Crear usuario | correcto, correo duplicado, nombre vacío |
| Listar usuarios | usuario creado, sin resultados, búsqueda extrema |
| Buscar usuario | encontrado, sin resultados, búsqueda vacía |
| Editar usuario | correcto, correo duplicado, nombre vacío |
| Eliminar usuario | correcto, inexistente (404), cancelado |

## Historias de usuario (Jira)

Proyecto gestionado en Jira ([angelj2992.atlassian.net](https://angelj2992.atlassian.net)),
una historia por funcionalidad con criterios de aceptación y de rechazo:

| Clave | Historia |
|-------|----------|
| KAN-1 | Iniciar sesión en la aplicación |
| KAN-2 | Crear un nuevo usuario |
| KAN-3 | Listar los usuarios registrados |
| KAN-4 | Buscar usuarios por nombre |
| KAN-5 | Editar los datos de un usuario |
| KAN-6 | Eliminar un usuario |

## Control de versiones

Repositorio: `ZeusRD55555/crud-selenium-itla-p3` (basado en
`ZeusRD55555/crud-gitflow-itla-p3`).
