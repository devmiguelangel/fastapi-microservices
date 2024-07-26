import json

import httpx

from api.settings import settings


class NotificationService:
    async def send_email(self, message: json):
        try:
            message = json.loads(message)
            audio_id = message['audio_id']

            return httpx.post(
                'https://api.mailgun.net/v3/sandboxd00602329e5d46ff8305b34fe30a1dea.mailgun.org/messages',
                auth=('api', settings.MAILGUN_API_KEY),
                data={'from': 'Excited User <mailgun@sandboxd00602329e5d46ff8305b34fe30a1dea.mailgun.org>',
                    'to': ['miguelangeldev@icloud.com', 'Miguel Angel'],
                    'subject': 'Hello',
                    'text': f'Audio ID: {audio_id} is now ready!'})
        except httpx.RequestError as e:
            print(e)
            return None
