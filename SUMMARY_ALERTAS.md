# Resumen de configuración de alertas

## Qué se hizo

- Se creó el archivo `alert_lambda.py` para usar en AWS Lambda.
- Se configuró el Lambda para enviar alertas por Telegram.
- Se ajustó el código para soportar uno o múltiples chat IDs de Telegram.
- Se documentó el uso de `TELEGRAM_CHAT_ID` y `TELEGRAM_CHAT_IDS`.
- Se identificó y explicó el error `HTTP Error 404: Not Found` de Telegram: suele deberse a un token inválido o mal formateado.

## Configuración actual

Variables de entorno necesarias en Lambda:

- `TELEGRAM_TOKEN`
- `TELEGRAM_CHAT_ID` o `TELEGRAM_CHAT_IDS`

Ejemplo para enviar a dos destinos:

```text
TELEGRAM_CHAT_IDS=8898523965,-5231385044
```

## Lo que se hizo (sesión 2026-05-25)

- Se agregó en `alert_lambda.py` el handler para eventos `RUNNING` de Step Functions: cuando alguien manda un mensaje, el Lambda envía una alerta con el número de teléfono y preview del mensaje.
- Se mejoró el handler de fallos para incluir el `status` (FAILED / TIMED_OUT / ABORTED) y el nombre de la state machine.
- Se desplegó el Lambda actualizado a AWS (`caboroMonitoreo`).
- **Regla EventBridge `Moon-NuevoMensaje`** — dispara al Lambda cada vez que inicia una ejecución (status=RUNNING) en Moon-dev-v4 o Moon-dev-v5.
- **Regla EventBridge `Moon-Fallos`** (paso 4) — dispara al Lambda cuando una ejecución falla (FAILED / TIMED_OUT / ABORTED) en Moon-dev-v4 o Moon-dev-v5.
- Se concedieron permisos de invocación a EventBridge sobre el Lambda.

## Próximos pasos

1. ~~Verificar token de Telegram~~ (completado en sesiones anteriores)

2. ~~Probar la API de Telegram~~ (completado en sesiones anteriores)

3. ~~Probar el Lambda con evento de prueba~~ (completado en sesiones anteriores)

4. ~~Reglas EventBridge para fallos~~ (completado 2026-05-25 — regla `Moon-Fallos`)

5. **Paso 5 pendiente:** Agregar alerta desde dentro del flujo cuando el usuario manda un 👎 (feedback negativo).
   - Requiere decidir cómo capturar el 👎: ¿como intent del router? ¿mensaje especial en caboroResponseDelivery?
   - La disponibilidad de datos (error HTTP_530) ya queda cubierta por la regla `Moon-Fallos` porque esos flujos terminan en `FinError`.

## Archivos relevantes

- `alert_lambda.py`
- `README.md`
- `SUMMARY_ALERTAS.md`
