// получение статуса игры каждые 5 секунд
$(function() {getStatusAjaxInterval()})

function getStatusAjaxInterval() {
    // получить список игроков и вставить их в шаблон
    const countdownTimer = setInterval(() => {

        $.ajax({
            url: getGameStatusApiURL(),
            type: 'get',
            dataType: 'json',
            cache: false,
            async: false,
            success: function (data) {
                console.log(data)
                relocation(data.status)
            },
            failure: function (data) {
                alert('getPlayersAjaxInterval - не удалось получить список игроков');
            }
        })
    }, 1000);
}


function relocation(status){
    console.log(status)
    let currentLocation = document.location.href
    console.log(currentLocation)
    let room_location;
    switch(status) {
        case 'created':
            room_location = getWaitingRoomURL()
            break;
        case 'start_timer':
            room_location = getTypingRoomURL()
            break;
        case 'typing':
            room_location = getTypingRoomURL()
            break;
        case 'waiting':
            // room_location = getWaitingTypingRoomURL()
            break;
        case 'looking':
            room_location = getResultRoomURL()
            break;
        case 'resulting':
            room_location = getResultListRoomURL()
            break;
        case 'ended':
            room_location = getGameOverRoomURL()
            break;
        // TODO наверно на главную
        case 'deleted':
            room_location = getGameOverRoomURL()
            break;
        default:
            // room_location = getMainRoomURL()
            alert("Пришел статус игры " + status)
            break;
    }

    if (status === 'waiting'){
        return;
    }

    let fullLocation = document.location.origin + room_location;
    console.log(fullLocation)
    if (currentLocation != fullLocation){
        $(location).attr('href',fullLocation);
    }
}

/////////////////////////////////
///////// API ///////////////
// function getGameStatusApiURL(){
//     return "{% url 'game_status_API' slug %}"
// }

