var username = "Anonymous";
var email = "anonymous";
var user_id = "anonymous";
var loggedIn = false;
$(document).ready(function () {
    initialize();
});
function initialize(){
    hideUserNavBoard();
    get_user_info();
}


function get_user_info() {
    console.log("in get_user_info()");
    var actionurl = "getuserinfo";
    var data = {};
    $.ajax({
        url: actionurl,
        cache: false,
        contentType: "application/json; charset=utf-8",
        processData: false,
        method: 'POST',
        dataType: 'json',
        data: JSON.stringify(data),
        success: function (response, status, jqXHR) {
            console.log('Status: ' + jqXHR.status);
            if (response != "no") {
                loggedIn = true;
                console.log(response);
                username = response.username;
                email = response.email;
                user_id = response.user_id;
                //If user is currently signed-in, show the user nav board on the rightmost side
                showUserNavBoard();
                $('#login-status').html(username + "<br>" + email);
                //window.location.href = 'index.html';
            }
            else {
                loggedIn = false;
                console.log("No user is logged in");
            }

        },
        error: (function (jqXHR, textStatus, errorThrown) {
            //alert(jqXHR.status + textStatus + errorThrown);
            console.log(jqXHR.status);
        })

    });
}
function signOut() {
    console.log("in signOut()");
    var actionurl = "signout";
    $.ajax({
        url: actionurl,
        cache: false,
        contentType: "application/json; charset=utf-8",
        processData: false,
        method: 'POST',
        dataType: 'json',
        success: function (response, status, jqXHR) {
            console.log('Status: ' + jqXHR.status);
            window.location.replace('landing.html')

        },
        error: (function (jqXHR, textStatus, errorThrown) {
            //alert(jqXHR.status + textStatus + errorThrown);
            console.log("ERROR: " + jqXHR.status);
            console.log(errorThrown);
        })

    });
}
function showUserNavBoard(){
    $('#user-nav-board').show();
    $('#default-user-nav-board').hide();
}
function hideUserNavBoard(){
    $('#user-nav-board').hide();
    $('#default-user-nav-board').show();
}
function isLoggedIn(){
    return loggedIn;
}