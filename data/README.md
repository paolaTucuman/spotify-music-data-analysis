# Datos del trabajo de Spotify

El archivo contiene **163.661 registros** y ocho columnas: nombre de la canción, artista, año, duración en milisegundos, popularidad, energía, *danceability* y tempo. Los años abarcan 1921–2020; 871 filas no tienen artista. Estas cifras describen el archivo del ejercicio, no la totalidad del catálogo de Spotify.

Extraje este archivo durante el módulo con una aplicación de mi cuenta de Spotify Developers. No conservo la fecha, la consulta ni el criterio exacto con que se seleccionaron las pistas. El CSV completo no se distribuye en este repositorio.

## Cómo se obtienen datos similares mediante la API

1. Crear una aplicación en [Spotify for Developers](https://developer.spotify.com/documentation/web-api/tutorials/getting-started) y consultar qué endpoints están disponibles para esa aplicación.
2. Solicitar un token de acceso. Para metadatos públicos que no pertenecen a una cuenta de usuario, Spotify documenta el flujo [Client Credentials](https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow).
3. Consultar los endpoints permitidos, por ejemplo búsqueda y detalles de pistas o artistas; paginar las respuestas cuando corresponda y seleccionar las columnas necesarias para formar una tabla.
4. Guardar las credenciales fuera del notebook y del repositorio. Antes de compartir datos o código, revisar los términos de la API y la procedencia de cada campo.

**Límite actual:** `energy`, `danceability` y `tempo` son características de audio. Spotify restringió el acceso a *Audio Features* para nuevos usos de la Web API desde noviembre de 2024. Por tanto, una aplicación creada hoy puede no obtener las mismas columnas ni reconstruir este archivo histórico. Véase el [anuncio de Spotify](https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api) y la [documentación de acceso](https://developer.spotify.com/documentation/web-api/concepts/authorization).
