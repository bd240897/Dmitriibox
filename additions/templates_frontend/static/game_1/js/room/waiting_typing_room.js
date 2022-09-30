
///////////// ПРИ ЗАПУСКЕ СТРАНИЦЫ ////////////////////

// получение списка игроков при заходе на страницу
$(function() {getPlayersAjax()})

// получение списка игроков каждые 5 секунд
$(function() {getPlayersAjaxInterval()})

// обновить список при клике на кнопку
$(".waiting-players-there-btn").click(function(){
    getPlayersAjax()
});

//////////////// МОИ ФУНКЦИИ /////////////////////

function getPlayersAjax() {
    // получить список игроков и вставить их в шаблон

    $.ajax({
        url: getUsersWaitingTypingRoomApiURL(),
        type: 'get',
        dataType: 'json',
        cache: false,
        success: function (data) {
            addPlayersThere(data_players=data)
        },
        failure: function (data) {
            alert('getPlayersAjax - не удалось получить список игроков');
        }
    })
}

function getPlayersAjaxInterval() {
    // получить список игроков и вставить их в шаблон
    const countdownTimer = setInterval(() => {

        $.ajax({
            url: getUsersWaitingTypingRoomApiURL(),
            type: 'get',
            dataType: 'json',
            cache: false,
            async: false,
            success: function (data) {
                addPlayersThere(data_players = data);
            },
            failure: function (data) {
                alert('getPlayersAjaxInterval - не удалось получить список игроков');
            }
        })
    }, 5000);
}

function addPlayersThere(data_players) {
    // добавить игроков в шаблон

    $('#waitingPlayersThere').empty()
    $('#playersThereTmpl').tmpl(data_players).appendTo('#waitingPlayersThere');
}


function redirectToResultRoom(){
    $(location).attr('href',getResultRoomURL());
}