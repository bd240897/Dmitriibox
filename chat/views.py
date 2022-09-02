# chat/views.py
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render

def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

def room_2(request, room_name):
    # Get channel_layer function
    import channels.layers

    # passing group_channel takes channel name
    channel_layer = channels.layers.get_channel_layer()
    # ch_group_list = channel_layer.group_channels('111')
    # print(ch_group_list)

    layer = get_channel_layer()
    async_to_sync(layer.group_send)('chat_111', {
        'type': 'chat_message',
        'message': "AAAAAAAAAAAAA"
    })


    return render(request, 'chat/room_2.html', {
        'room_name': room_name
    })