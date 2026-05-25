import json
import os
import urllib.request
from datetime import datetime

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
TELEGRAM_CHAT_IDS = os.environ.get('TELEGRAM_CHAT_IDS')


def get_telegram_chat_ids():
    ids = []
    if TELEGRAM_CHAT_IDS:
        ids += [item.strip() for item in TELEGRAM_CHAT_IDS.split(',') if item.strip()]
    if TELEGRAM_CHAT_ID:
        ids.append(TELEGRAM_CHAT_ID.strip())
    return list(dict.fromkeys(ids))


def send_telegram_message(chat_id: str, text: str):
    if not TELEGRAM_TOKEN or not chat_id:
        raise ValueError('TELEGRAM_TOKEN and at least one chat_id must be set')

    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        resp.read()


def send_alert(title: str, message: str, severity: str = 'INFO'):
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    emoji = '🔴' if severity == 'ERROR' else '⚠️' if severity == 'WARNING' else '✅'
    telegram_text = f"{emoji} *{title}*\n{message}\n\n_Enviado:_ {timestamp}"
    chat_ids = get_telegram_chat_ids()

    if not chat_ids:
        raise ValueError('No Telegram chat IDs configured')

    for chat_id in chat_ids:
        try:
            send_telegram_message(chat_id, telegram_text)
        except Exception as e:
            print(f'Telegram error [{chat_id}]: {e}')


def lambda_handler(event, context):
    print('Received event:', json.dumps(event))

    alert_type = event.get('alert_type')

    if event.get('source') == 'aws.states':
        detail = event.get('detail', {})
        status = detail.get('status', '')
        sm_name = detail.get('stateMachineArn', '').split(':')[-1]

        if status == 'RUNNING':
            title = 'Mensaje nuevo recibido'
            execution_input = detail.get('input', '{}')
            try:
                input_data = json.loads(execution_input) if isinstance(execution_input, str) else execution_input
            except Exception:
                input_data = {}
            from_number = input_data.get('from_number', 'desconocido')
            msg_text = input_data.get('message', '')
            preview = (msg_text[:120] + '…') if len(msg_text) > 120 else msg_text
            message = (
                f"De: {from_number}\n"
                f"Mensaje: {preview}\n"
                f"Ejecución: {detail.get('name', 'desconocido')}"
            )
            send_alert(title, message, severity='INFO')

        elif status in ('FAILED', 'TIMED_OUT', 'ABORTED'):
            title = f'Fallo en Step Functions'
            message = (
                f"Estado: {status}\n"
                f"Machine: {sm_name}\n"
                f"Error: {detail.get('error', 'no disponible')}\n"
                f"Causa: {detail.get('cause', 'no disponible')}"
            )
            send_alert(title, message, severity='ERROR')

    elif alert_type == 'data_unavailable':
        title = 'Datos no disponibles'
        message = (
            f"Endpoint: {event.get('api_endpoint', 'desconocido')}\n"
            f"Error: {event.get('error', 'no disponible')}"
        )
        send_alert(title, message, severity='WARNING')
    elif alert_type == 'user_feedback':
        title = 'Feedback negativo del usuario'
        message = (
            f"Usuario: {event.get('user_id', 'desconocido')}\n"
            f"Feedback: {event.get('feedback', 'no disponible')}\n"
            f"Contexto: {event.get('context', 'sin contexto')}"
        )
        send_alert(title, message, severity='WARNING')
    else:
        title = 'Alerta genérica'
        message = json.dumps(event, ensure_ascii=False, indent=2)
        send_alert(title, message, severity='INFO')

    return {'statusCode': 200, 'body': 'Alerta enviada'}
