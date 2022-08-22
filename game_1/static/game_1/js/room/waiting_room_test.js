
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
        url: getUsersWaitingRoomApiURL(),
        type: 'get',
        dataType: 'json',
        cache: false,
        async: false,
        success: function (data) {
            console.log(data)
            addPlayersThere(data_players=data);
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
            url: getUsersWaitingRoomApiURL(),
            type: 'get',
            dataType: 'json',
            cache: false,
            async: false,
            success: function (data) {
                addPlayersThere(data_players = data);
                if (data.gameroom.status_game === true) {
                    clearInterval(countdownTimer)
                    // renderTimeTmp()
                    // ProgressCountdown(10, 'pageBeginCountdown', 'pageBeginCountdownText').then(data => {
                    //     redirectToTypingRoom()
                    // })
                    redirectToTypingRoom()

                }
            },
            failure: function (data) {
                alert('getPlayersAjaxInterval - не удалось получить список игроков');
            }
        })
    }, 5000);
}

function renderTimeTmp(){
    $('#waitingPlayersThere').empty()
    $('#TimerTmpl').tmpl().appendTo('#waitingPlayersThere');
}

async function ProgressCountdown(timeleft, bar, text) {
    // обратный отсчет
    return await new Promise((resolve, reject) => {
        renderTimeTmp()

        var countdownTimer = setInterval(() => {
            timeleft--;

            document.getElementById(bar).value = timeleft;
            document.getElementById(text).textContent = timeleft;

            if (timeleft <= 0) {
                console.log("Отсчет закончен")
                clearInterval(countdownTimer);
                resolve(true);
            }
        }, 1000);
    });
}

// данные для теста
var DATA_PLAYERS =
    {'test':
            [
                {username: 'Dima',},
                {username: 'Masha',}
            ]
    };

function addPlayersThere(data_players) {
    // добавить игроков в шаблон

    $('#waitingPlayersThere').empty()
    $('#playersThereTmpl').tmpl(data_players).appendTo('#waitingPlayersThere');
}


function redirectToTypingRoom(){
    // проверит начата ил игра и перенаправит всех пользователей на typing rom
    // косытьль - нужно делать пост запрос с параметром юзера, и если его игра началась то редиректить его
    $(location).attr('href',getTypingRoomApiURL());
}


