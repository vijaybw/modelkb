$(document).ready(function () {
    $("#projectPanel").hide();
    get_user_models();
});


function get_user_models() {
    console.log("in get_user_models()");
    var actionurl = "getuserModels";
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
                console.log(response);
                display_info(response.user);
                display_models(response);
            }
            else {
                console.log("No user is logged in");
            }

        },
        error: (function (jqXHR, textStatus, errorThrown) {
            //alert(jqXHR.status + textStatus + errorThrown);
            console.log(jqXHR.status);
        })

    });
}
function display_info(user){
    $(".username").text(user.fname + " " + user.lname);
    $(".email").text(user.email);
}
function display_models(response) {
    console.log(response.models.length);
    for (var i = 0; i < response.models.length; i++) {
        console.log(response.models[i]);
        var newPanel = $('#projectPanel').clone();
        var newPanelID = response.models[i].shortname.toString();
        newPanel.show();
        newPanel.attr("id", "projectPanel" + i);
        newPanel.appendTo($("#projectBoard"));
        $("#projectPanel" + i + ' .fixed_name').text(response.models[i].longname);
        $("#projectPanel" + i + ' a').attr("id", newPanelID);
        $("#projectPanel" + i + ' a').attr('href','/empty.html?id=' + newPanelID + '&fullname=' + response.models[i].longname);
        $("#projectPanel" + i + ' .fixed_description').text(response.models[i].description);
        $("#projectPanel" + i + ' .owner-actual').text(response.user.fname + " " + response.user.lname);
        //Click Listener for Div
        $( "#projectPanel" + i ).click(function() {
            location.href= $(this).find('a').attr("href");
        });
    }
}