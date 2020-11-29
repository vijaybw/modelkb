$(document).ready(function () {
    $("#login_btn").click(function (event) {
        console.log('login clicked!');
        var email = $("#email2").val();
        var password = $("#pwd2").val();
        var data = {};
        data.email = email;
        data.password = password;
        console.log(email);
        console.log(password);
        var actionurl = "signin";
        var form = document.getElementById('login_form');
        //Check whether all fields have been filled out
        for(var i=0; i < form.elements.length; i++){
            if(form.elements[i].value === '' && form.elements[i].hasAttribute('required')){
                //alert('There are some required fields!');
                return false;
            }
        }

        $.ajax({
            url: actionurl,
            cache: false,
            contentType: "application/json; charset=utf-8",
            processData: false,
            method: 'POST',
            dataType: 'json',
            data: JSON.stringify(data),
            success: function (response, status, jqXHR) {
                console.log('in success ' + jqXHR.status);
                console.log(response);
                window.location.href = 'category-page.html';

            },
            error: (function (jqXHR, textStatus, errorThrown) {
                //alert(jqXHR.status + textStatus + errorThrown);
                console.log(errorThrown);
            })

        });
    });
    $("#signup_btn").click(function (event) {
        console.log('signup clicked!');
        var fname = $("#fname").val();
        var lname = $("#lname").val();
        var email = $("#email").val();
        var password = $("#pwd").val();
        var data = {
            fname: fname,
            lname: lname,
            email: email,
            password: password,
        };

        console.log(email);
        console.log(password);
        var actionurl = "signup";
        var form = document.getElementById('signup_form');
        //Check whether all fields have been filled out
        for(var i=0; i < form.elements.length; i++){
            if(form.elements[i].value === '' && form.elements[i].hasAttribute('required')){
                // alert('There are some required fields!');
                return false;
            }
        }

        $.ajax({
            url: actionurl,
            cache: false,
            contentType: "application/json; charset=utf-8",
            processData: false,
            method: 'POST',
            dataType: 'json',
            data: JSON.stringify(data),
            success: function (response, status, jqXHR) {
                console.log('in success ' + jqXHR.status);
                console.log(response);
                window.location.href = 'landing.html';

            },
            error: (function (jqXHR, textStatus, errorThrown) {
                //alert(jqXHR.status + textStatus + errorThrown);
                console.log(errorThrown);
            })

        });
    });
    function get_user_info(){
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
                if (response != "no"){
                    window.location.href = 'category-page.html';
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
    function init(){
        get_user_info();
    }
    init();
});