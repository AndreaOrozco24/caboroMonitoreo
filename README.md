# Sistema de Alertas AWS

Este pequeño repositorio contiene un Lambda para enviar alertas a Telegram.

## Archivos

- `alert_lambda.py`: función Lambda que envía alertas a Telegram.

## Variables de entorno necesarias

- `TELEGRAM_TOKEN`
- `TELEGRAM_CHAT_ID` o `TELEGRAM_CHAT_IDS`

## Uso

1. Crea un Lambda en AWS con `alert_lambda.lambda_handler`.
2. Configura las variables de entorno.
   - Usa `TELEGRAM_CHAT_ID` si quieres un solo destinatario.
   - Usa `TELEGRAM_CHAT_IDS` con una lista separada por comas si quieres varios destinatarios.
3. En CloudWatch Events, crea una regla para detectar fallos en Step Functions que apunte a este Lambda.

## Varias personas / varios teléfonos

- Si quieres que la alerta llegue a dos personas diferentes, crea dos chat_ids y configura:

  ```text
  TELEGRAM_CHAT_IDS=8898523965,1234567890
  ```

- Si prefieres enviar a un grupo donde ya están las dos personas, usa el chat_id del grupo en `TELEGRAM_CHAT_ID`.

- Para obtener un `chat_id` adicional, cada persona debe iniciar el bot y luego consultar `getUpdates` con el token.

## Ejemplo de evento para pruebas

```json
{
  "alert_type": "user_feedback",
  "user_id": "8898523965",
  "feedback": "El modelo respondió mal",
  "context": "Consulta de disponibilidad"
}
```
