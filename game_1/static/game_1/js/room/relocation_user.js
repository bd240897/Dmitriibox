
function relocation(status) {
    console.log('user ', status)
    let currentLocation = document.location.href
    console.log(currentLocation)
    let room_location;
    switch (status) {
        case 'waiting_room':
            room_location = getWaitingRoomURL()
            break;
        case 'typing_room':
            // TODO если обычный юзер напечатао раньше адмимна то его будет кидать туда сюда
            room_location = getTypingRoomURL()
            break;
        case 'waiting_typing_room':
            // TODO если админ напечатал раньше обычного юзера то все перекинет сюда
            // room_location = getWaitingTypingRoomURL()
            break;
        case 'result_room':
            room_location = getResultRoomURL()
            break;
        case 'result_list_room':
            room_location = getResultListRoomURL()
            break;
        case 'gameover_room':
            room_location = getGameOverRoomURL()
            break;
        default:
            // room_location = getMainRoomURL()
            alert("Пришел статус игры " + status)
            break;
    }

    if (status === 'waiting_typing_room') {
        return;
    }

    let fullLocation = document.location.origin + room_location;
    console.log(fullLocation)
    if (currentLocation != fullLocation) {
        $(location).attr('href', fullLocation);
    }
}

