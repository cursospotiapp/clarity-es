# Rotar la clave

Es importante señalar que los siguientes pasos son fundamentales para realizar el proceso.

1. Procede a crear la clave de sustitución.
2. Lleva a cabo su despliegue en staging.
3. Realiza la verificación de una petición firmada con `keys verify --env staging`.
4. Procede a revocar la clave anterior.

> Advertencia: revocar primero provoca una interrupción del servicio.

Consulta la [referencia de claves](https://example.com/keys).
