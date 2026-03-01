# Guía de Interconexión: Frontend y Backend (Angular + Django)

Este documento explica cómo están vinculados los archivos del proyecto y cómo fluye la información desde la interfaz de usuario (`app.html`) hasta el servidor de base de datos (`Django`).

## 1. El Flujo de una Petición (De Angular a Django)

Imagina que el usuario entra a la página. El camino que sigue la información es este:

1.  **Vista (`app.html`)**: Muestra un mensaje que está guardado en una variable llamada `message()`.
2.  **Controlador (`app.ts`)**: Al cargar, le pide al "servicio" que traiga el mensaje del servidor.
3.  **Servidor de Mensajería (`api.service.ts`)**: Lanza la petición HTTP a la dirección `/api/hello/`.
4.  **El Puente (`proxy.conf.json`)**: Detecta que la petición empieza con `/api` y la redirige al servidor de Django (`http://localhost:8000`).
5.  **El Portero de Django (`backend/urls.py`)**: Recibe la petición y ve que empieza con `api/`, así que se la pasa a la aplicación `api`.
6.  **El Letrero de la App (`api/urls.py`)**: Ve que después de `api/` viene `hello/`, y sabe que debe llamar a la función `hello_world`.
7.  **El Cerebro (`api/views.py`)**: Ejecuta la función `hello_world`, genera la respuesta (un JSON con el mensaje) y la envía de vuelta por el mismo camino.

---

## 2. Archivos Vinculados Detalladamente

### A. Lado del Frontend (Angular)

*   **`src/app/app.html`**:
    *   **Función**: Es la cara visible.
    *   **Vínculo**: Usa `{{ message() }}` para mostrar el contenido que el controlador (`app.ts`) trajo del backend.
    *   **Directiva `@if`**: Controla si muestra el mensaje o un texto de "Cargando...".

*   **`src/app/app.ts` (Componente `App`)**:
    *   **Función**: Orquesta la lógica de la página principal.
    *   **Vínculo**:
        1. Inyecta el `ApiService`.
        2. En `ngOnInit` (cuando arranca el componente), llama a `apiService.getHello()`.
        3. Cuando recibe el dato, usa `this.message.set(data.message)` para actualizar lo que el HTML está mostrando.

*   **`src/app/services/api.service.ts`**:
    *   **Función**: Centraliza todas las llamadas al servidor.
    *   **Vínculo**: Usa `HttpClient` para hacer un `GET` a la ruta `/api/hello/`. No necesita poner `http://localhost:8000` porque el proxy se encarga de eso.

---

### B. La Conexión (El "Pegamento")

*   **`proxy.conf.json`**:
    *   **Función**: Evita errores de CORS (seguridad del navegador) y permite que Angular hable con Django como si estuvieran en el mismo lugar.
    *   **Vínculo**: Dice: "Todo lo que vaya a `/api` mándalo a `http://localhost:8000`".

*   **`angular.json`**:
    *   **Vínculo**: En la sección `architect -> serve -> options`, tiene configurado `"proxyConfig": "proxy.conf.json"`. Esto activa el puente cuando corres `npm start`.

---

### C. Lado del Backend (Django)

*   **`backend/urls.py`**:
    *   **Función**: Es el mapa principal del servidor.
    *   **Vínculo**: Tiene la línea `path('api/', include('api.urls'))`, que conecta las URLs globales con las específicas de tu aplicación `api`.

*   **`api/urls.py`**:
    *   **Función**: Mapa específico de la app de base de datos.
    *   **Vínculo**: Tiene la línea `path('hello/', hello_world, name='hello_world')`, que vincula la ruta de la URL con la función en el archivo de vistas.

*   **`api/views.py`**:
    *   **Función**: Donde ocurre la magia (la lógica de negocio).
    *   **Vínculo**: La función `hello_world` devuelve un `JsonResponse({"message": "el pepe", ...})`. Ese `"message": "el pepe"` es el que termina apareciendo en tu `app.html`.

---

## 3. ¿Cómo añadir una nueva conexión? (Ejemplo: "Precios")

Si quieres mostrar una lista de precios, harías esto:

1.  **Django (`api/views.py`)**: Creas una función `get_precios(request)` que devuelva los datos.
2.  **Django (`api/urls.py`)**: Añades `path('precios/', get_precios, name='precios')`.
3.  **Angular (`api.service.ts`)**: Añades una función `getPrecios() { return this.http.get('/api/precios/'); }`.
4.  **Angular (`app.ts`)**: Llamas a ese nuevo método y guardas el resultado en una señal (signal).
5.  **Angular (`app.html`)**: Usas un `@for` para mostrar la lista de precios.

¡Y listo! Todo está conectado de punta a punta.
