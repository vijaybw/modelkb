$(document).ready(function () {

    $("#projectPanel").hide();
    var url = 'pArchiveFirebase';
    $.ajax({
        url: url,
        method: 'POST',
        dataType: 'json'
    }).done(function (response) {
        $('#result').text("");
        console.log(response.project.length);
        for (var i = 0; i < response.project.length; i++) {
            console.log(response.project[i]);
            var newPanel = $('#projectPanel').clone();
            var newPanelID = response.project[i].name.toString();
            newPanel.show();
            newPanel.attr("id", "projectPanel" + i);
            newPanel.appendTo($("#projectBoard"));

            $("#projectPanel" + i + ' .fixed_name').text(response.project[i].fullname);
            $("#projectPanel" + i + ' a').attr("id", newPanelID);
            $("#projectPanel" + i).attr('href','/model-page.html?id=' + newPanelID + '&fullname=' + response.project[i].fullname+ '&m_id=' + response.project[i].m_id);
            $("#projectPanel" + i + ' .fixed_description').text(response.project[i].description);
            $("#projectPanel" + i + ' .owner-actual').attr("href", "user_profile_public.html?id=" + response.project[i].create_user_id);
            $("#projectPanel" + i + ' .owner-actual').text(response.project[i].create_username);
            //Click Listener for Div
            $( "#projectPanel" + i ).click(function() {
                location.href= $(this).attr("href");
            });
            loadModelImg("projectPanel" + i, response.project[i].name)
            updateRatingUI("projectPanel" + i, response.project[i].rating);

        }
    }).fail(function () {
        alert("Sorry. Server unavailable. ");
    });


    function loadModelImg(panelID, projectName){
        console.log(panelID + " " + projectName);
        var modelImg = $("#" + panelID + " .model-img");
        var imgSrc = "./tmp/" + projectName + '/logo.jpeg';
        modelImg.attr("src", imgSrc );
        console.log("Current Src:" + modelImg.attr('src'));
        modelImg.on("error", function(){
            var imgSrc = "./tmp/" + projectName + '/logo.jpg';
            modelImg.attr("src", imgSrc );
            console.log(imgSrc + "not found");
        })

    }
    function updateRatingUI(panelID, ratingArr) {
        function roundHalf(num) {
            return Math.round(num*2)/2;
        }
        function getSum(total, num) {
            return total + num;
        }
        if (ratingArr.length !== 0){
            console.log((ratingArr.reduce(getSum))/ratingArr.length);
            console.log(roundHalf((ratingArr.reduce(getSum))/ratingArr.length));
            var avgRating = roundHalf((ratingArr.reduce(getSum))/ratingArr.length);
            console.log("average rating of this model: " + avgRating);
            var wholeStarNum, wholeStarLeft;
            //avgRating = 5;
            var halfStar = false;
            if (avgRating%1 == 0.5){
                wholeStarNum = avgRating - 0.5;
                wholeStarLeft = 5 - wholeStarNum - 1;
                halfStar = true;

            }
            else {
                wholeStarNum = avgRating;
                wholeStarLeft = 5 - wholeStarNum;
            }

            //Render Actual Star Components on UI
            for (var i = 0; i < wholeStarNum; i++){
                $("#" + panelID + " .rating").append("<i class=\"fas fa-star checked\"></i>\n")
            }
            if (halfStar == true){
                $("#" + panelID + " .rating").append("<i class=\"fas fa-star-half-alt checked\"></i>\n")
            }
            for (var i = 0; i < wholeStarLeft; i++){
                $("#" + panelID + " .rating").append("<i class=\"fas fa-star\"></i>\n")
            }
        }
        else {
            for (var i = 0; i < 5; i++){
                $("#" + panelID + " .rating").append("<i class=\"fas fa-star\"></i>\n")
            }
        }
    }
});