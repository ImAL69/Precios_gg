# Gg - Proyecto Fullstack (Angular + Django)

Este proyecto combina un frontend de Angular con un backend de Django, configurados para comunicarse mediante un proxy de desarrollo.

## Requisitos Previos

- Node.js y npm
- Python 3.x
- Entorno virtual configurado (ya existe la carpeta `venv`)

## Servidor de Desarrollo (Frontend)

Para iniciar el servidor de desarrollo de Angular, ejecuta:

```bash
npm start
```

La aplicación estará disponible en `http://localhost:4200/`. Las llamadas a `/api/*` se redirigirán a `http://localhost:8000/`.

## Servidor de Backend (Django)

Para iniciar el servidor de Django:

1. Activa el entorno virtual:
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

2. Ejecuta el servidor:
   ```bash
   python manage.py runserver
   ```

El backend estará disponible en `http://localhost:8000/`. El endpoint de prueba está en `http://localhost:8000/api/hello/`.

## Estructura del Proyecto

- `src/`: Código fuente de Angular.
- `api/`: Aplicación de Django para la lógica de la API.
- `backend/`: Configuración principal del proyecto Django.
- `proxy.conf.json`: Configuración del proxy para evitar CORS en desarrollo.

## Tailwind CSS

El proyecto utiliza **Tailwind CSS v4**. A diferencia de versiones anteriores, la configuración se maneja directamente en los archivos CSS.

### Uso y Configuración

1. **Estilos Globales**: Tailwind está importado en `src/styles.css` con la directiva `@import "tailwindcss";`.
2. **Clases de Utilidad**: Puedes usar cualquier clase de Tailwind directamente en tus plantillas HTML (como se ve en `src/app/app.html`).
3. **Personalización**: Si necesitas personalizar el tema (colores, fuentes, etc.), puedes hacerlo directamente en `src/styles.css` usando la directiva `@theme`:

   ```css
   @theme {
     --color-primary: #3b82f6;
     --font-sans: 'Inter', sans-serif;
   }
   ```

No es necesario un archivo `tailwind.config.js`, aunque sigue siendo compatible si prefieres el formato antiguo.

> **Tip**: Se recomienda instalar la extensión **Tailwind CSS IntelliSense** en VS Code para obtener autocompletado y sugerencias de clases.

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Vitest](https://vitest.dev/) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
