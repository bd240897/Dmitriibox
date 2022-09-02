from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_to_channel_layer(room_code='SQPQ', msg='AAAAA1111'):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(room_code, {
        'type': 'chat_message',
        'message': msg,
        'action': 'MOVE'
    })