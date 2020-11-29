var host, protocol, projectName, fullpName, mID;
var modelURL;
var imgName;
var ratingIndex = -1;
$(document).ready(function () {
    console.log("init fire!");
    console.log(localStorage.getItem("pName"));
    init();
    $('#fileInput').on('change', function(){
        var control = $('#inputFileMaskText');
        control.val(this.files[0].name);
    });

    $('#fileInput2').on('change', function(){
        console.log("in file input2");
        var control = $('#inputFileMaskText2');
        control.val(this.files[0].name);
        imgName = this.files[0].name;
        console.log('img name: ' + imgName);
        //set listener for uploadBtn
        if (imgName.substr(imgName.length-4,4) != '.csv'){
            readURL(this);
        }
        else {
            $('#img-container').hide();
        }

    });
    $("#fileInputMask").click(function() {
        $('#fileInput2').click();
    });
    $("#uploadBtn").click(function (event) {
        console.log('inupload!')
        var fileName;
        //Input Validation
        if ($('#fileInput2')[0].files[0] == undefined){
            alert("Please select an image!!!");
        }
        //if image is valid
        else {
            imgName = $('#fileInput2')[0].files[0].name;
            uploadImage();

            //console.log($('#fileInput2')[0].files[0].name);

        }


    });
    function getDescription(pName) {
        console.log('in client getDescription' + pName);
        var data = {};
        data.pname = pName;
        var actionurl = "getDescription";
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
                $(".model-description").text(response.description);
                $(".owner").text(response.create_username);

            },
            error: (function (jqXHR, textStatus, errorThrown) {
                //alert(jqXHR.status + textStatus + errorThrown);
                window.location.replace('404.html')
            })

        });
    }

    function updateRatingUI(ratingArr) {
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
                $(".rating").append("<i class=\"fas fa-star checked\"></i>\n")
            }
            if (halfStar == true){
                $(".rating").append("<i class=\"fas fa-star-half-alt checked\"></i>\n")
            }
            for (var i = 0; i < wholeStarLeft; i++){
                $(".rating").append("<i class=\"fas fa-star\"></i>\n")
            }
        }
        else {
            return 0;
        }
    }

    function getDescriptionFirebase(m_id) {
        console.log('in client getDescription' + m_id);
        var data = {};
        data.m_id = m_id;
        var actionurl = "getDescriptionFirebase";
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
                $(".model-description").text(response.description);
                $(".owner").text(response.create_username);
                updateRatingUI(response.rating);

            },
            error: (function (jqXHR, textStatus, errorThrown) {
                alert(jqXHR.status + textStatus + errorThrown);
                //window.location.replace('404.html')
            })

        });
    }
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#uploadBtn').show();
                $('#previewImg').show();
                $('#img-container').show();
                $('#previewImg').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }
    function init(){
        /*Hide all the show-on-click elements */
        $('#uploadBtn').hide();
        $('#previewImg').hide();
        $('.result').hide();
        $('#img-container').hide();
        $('#loading-screen').hide();
        $('#discussion-card').hide();
        //enableDiscussBtnListener("http://127.0.0.1:8080/discussion.html?id=EnlargenHeart&testid=testcase-1558044562577&imgname=xray.jpg&m_id=AeOxsBsMXGJCSDtez8Sj");
        enableRatingListener();
        console.log(window.location.pathname);
        console.log(window.location.href);
        var fullURL = window.location.href;
        var url = new URL(fullURL);
        host = url.host;
        protocol = url.protocol;
        var newurl = protocol + "://" + host + "/discussion.html?id=EnlargenHeart&testid=testcase-1558044562577&imgname=xray.jpg&m_id=AeOxsBsMXGJCSDtez8Sj"
        console.log(protocol);
        fullpName = url.searchParams.get("fullname");
        projectName = url.searchParams.get("id");
        mID = url.searchParams.get("m_id");
        //console.log(fullURL.substring(fullURL.lastIndexOf("=")+1));
        var requiredDisplayPath = '/model-page.html';

        loadModelImg();
        if (window.location.pathname == requiredDisplayPath
            && projectName != null
            && projectName != "")
        {
            $(".model-name").html(fullpName + "<small> Model </small>");
            modelURL= '/predict?id=' + projectName;
            //getDescription(projectName);
            getDescriptionFirebase(mID);
        }
        loadDiscussionPosts(mID);
    }

    function uploadImage(img){
        //Turn on loading icon
        $("#loading-screen").show();
        $(".result").hide();
        //Ajax Call to Server
        var actionurl = "fileupload";
        var data = new FormData();
        jQuery.each(jQuery('#fileInput2')[0].files, function (i, file) {
            console.log('in append');
            console.log(file);
            data.append('filetoupload', file);
        });
        data.append('pname', projectName);
        data.append('m_id', mID);

        //do your own request an handle the results
        $.ajax({
            url: actionurl,
            cache: false,
            contentType: false,
            processData: false,
            method: 'POST',
            data: data,
            success: function (response, status, jqXHR) {
                console.log('in success ' + jqXHR.status);
                runModel(modelURL);

            },
            error: (function (jqXHR, textStatus, errorThrown) {
                //alert(jqXHR.status + textStatus + errorThrown);
                window.location.replace('404.html')
            })

        });
    }

    function runModel(url){
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            data: {imgname: imgName}
        }).done(function (response) {
            console.log(response);
            var projectName = response[0].projectName;
            var testID = response[0].testcaseNum;
            var imgName = response[0].imgName;
            var shareURL = protocol + "//" + host + "/discussion.html?id=" + projectName + '&testid=' + testID + "&imgname=" + imgName + "&m_id=" + mID;
            var discussURL = protocol + "//" + host + "/discussion.html?id=" + projectName + '&testid=' + testID + "&imgname=" + imgName + "&m_id=" + mID;
            var testcaseURL = './tmp/' + projectName + '/' + testID + '/' + imgName;

            $("#share-btn").attr("href", shareURL);
            enableDiscussBtnListener(discussURL);
            $('#loading-screen').hide();
            $('.result').show();
            enableRatingListener();

            // //Update Preview Image ID
            // $("#previewImg").attr("testcaseID", testID);
            // setPreviewListener();



            //Chart Visualization
            $("#chart").empty();
            var chartData =[], xAxis = [];
            //First index is information for Test Case Num, Image Name, and Project Name
            for (i=1;i<response.length;i++){
                chartData.push(response[i].value * 100);
                xAxis.push(response[i].classname);
            }

            ///Chart Section
            var chartHeight=130 + 40* (response.length-1); //minus the first object which is irrelevant
            console.log("Chart Height: " + chartHeight);
            var options = {
                chart: {
                    height: chartHeight,
                    type: 'bar'
                },
                plotOptions: {
                    bar: {
                        barHeight: '100%',
                        distributed: true,
                        horizontal: true,
                        dataLabels: {
                            position: 'bottom'
                        },
                    }
                },
                colors: ['#33b2df', '#546E7A', '#d4526e', '#13d8aa', '#A5978B', '#2b908f', '#f9a3a4', '#90ee7e', '#f48024', '#69d2e7'],
                dataLabels: {
                    enabled: true,
                    textAnchor: 'start',
                    style: {
                        colors: ['#fff']
                    },
                    formatter: function(val, opt) {
                        return val.toFixed(2);
                    },
                    offsetX: 0,
                    dropShadow: {
                        enabled: true
                    }
                },
                series: [{
                    name: "Probability",
                    data: chartData
                }],
                stroke: {
                    curve: 'smooth',
                    width: 0.5,
                    colors: ['#fff']
                },
                xaxis: {
                    categories: xAxis,
                    title: {
                        text: 'Probability'
                    },
                    labels: {
                        formatter: function(val) {
                            return (Math.abs(Math.round(val)))
                        }
                    }
                },
                yaxis: {
                    min: 0,
                    max: 100,
                    decimalsInFloat: 2,
                    labels: {
                        show: true
                    }
                },
                title: {
                    text: 'Prediction Result',
                    align: 'center',
                    floating: true
                },
                subtitle: {
                    text: 'Model: ',
                    align: 'center',
                },
                tooltip: {
                    theme: 'dark',
                    shared: false,
                    x: {
                        formatter: function(val) {
                            return val
                        }
                    },
                    y: {
                        formatter: function(val) {
                            return Math.abs(val)/100
                        }
                    }
                }
            };

            var chart = new ApexCharts(
                document.querySelector("#chart"),
                options
            );

            chart.render();



        }).fail(function () {
            alert("Sorry. Server unavailable. ");
            window.location.replace('404.html')
        });
    }
    function parseDate(str){
        var originalDate = str.toString();
        var parsedDate = originalDate.slice(0, originalDate.indexOf('GMT'));
        return parsedDate;
    }

    function loadModelImg(){
        modelImg = $(".model-img");
        var imgSrc = "./tmp/" + projectName + '/logo.jpeg';
        modelImg.attr("src", imgSrc );
        console.log(imgSrc);
        console.log("Current Src:" + modelImg.attr('src'));
        modelImg.on("error", function(){
            var imgSrc = "./tmp/" + projectName + '/logo.jpg';
            modelImg.attr("src", imgSrc );
            console.log("logo not found");
        })

    }

    function loadDiscussionPosts(m_id){
        console.log('in loadDiscussionPosts' + m_id);
        var data = {};
        data.m_id = m_id;
        var actionurl = "getDiscussionPostsInfo";
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

                if (response.length != 0 ){
                    for (var i = 0; i < response.length; i++){
                        var newDiscussionCard = $("#discussion-card").clone();
                        if (response[i].preview_img_name != ""){
                            var previewImgURL = './tmp/' + projectName + '/' + response[i].testcasenum+ '/' + response[i].preview_img_name;
                            newDiscussionCard.find(".discussion-preview-img").attr("src", previewImgURL);
                        }

                        newDiscussionCard.attr("discuss-id", response[i].discuss_id);
                        newDiscussionCard.attr("id", response[i].discuss_id);
                        //TODO: Make a function to retrieve the preview images for discussion.
                        //Use Firebase Storage if possible
                        // newDiscussionCard.find(".discussion-preview-img").attr("src",);
                        newDiscussionCard.find(".discussion-title").text(response[i].question);
                        newDiscussionCard.find(".discussion-owner").text(response[i].owner);
                        newDiscussionCard.find(".discussion-date").text(response[i].create_date);

                        if (typeof(response[i].comments) !== "undefined"){
                            newDiscussionCard.find(".discussion-comment-num").text(response[i].comments.length);
                        }
                        else {
                            newDiscussionCard.find(".discussion-comment-num").text(0);
                        }
                        var testcaseURL = protocol + "//" + host + "/discussion.html?id=" + projectName
                            + "&testid=" + response[i].testcasenum
                            + "&imgname=" + response[i].preview_img_name
                            + "&m_id=" + mID
                            + "&discuss_id=" + response[i].discuss_id;
                        newDiscussionCard.attr("href", testcaseURL);
                        newDiscussionCard.click(function(){
                            window.location.href = $(this).attr("href");
                        });
                        newDiscussionCard.show();
                        $("#discussion-panel").append(newDiscussionCard);

                    }
                }


            },
            error: (function (jqXHR, textStatus, errorThrown) {
                alert(jqXHR.status + textStatus + errorThrown);
                //window.location.replace('404.html')
            })

        });
    }
    function enableRatingListener(){
        $("#rating-btn").show();
        $("#rating-submit-btn").click(function(){
            var rating = $("#rating_val").val();
            var data = {
                rating_index: ratingIndex,
                rating: rating,
                model_id: mID
            };
            console.log(data);
            //Ajax Call to Server
            var actionurl = "saveNewRating";

            //do your own request an handle the results
            $.ajax({
                url: actionurl,
                cache: false,
                contentType: "application/json; charset=utf-8",
                processData: false,
                method: 'POST',
                data: JSON.stringify(data),
                dataType: 'json',
                success: function (response, status, jqXHR) {
                    console.log('in success ' + jqXHR.status);
                    ratingIndex = response.rating_index;
                    console.log("Current Rating Index: " + ratingIndex );
                },
                error: (function (jqXHR, textStatus, errorThrown) {
                    console.log(jqXHR.status + textStatus + errorThrown);
                    //window.location.replace('404.html')
                })

            });
        });
    }
});
function enableDiscussBtnListener(discussURL){
    console.log("In enablediscussListener()");
    $(".discussion-input").hide();
    $("#discuss-btn").click(function(){
        $(".discussion-input").show();
    });
    enableDiscussSubmitListener(discussURL)

}
function enableDiscussSubmitListener(discussURL){
    console.log(discussURL);
    var url = new URL(discussURL);
    var projectName = url.searchParams.get("id");
    var testcaseNum = url.searchParams.get("testid");
    var imgName = url.searchParams.get("imgname");
    $("#discuss-submit").click(function(){
        var discussText = $(".discussion-input input").val();
        if (discussText === ""){
            alert("Discussion Question cannot be empty!");
        }
        else {
            console.log('in client enableDiscussSubmitListener');
            var data = {
                username: username,
                user_id: user_id,
                projectName: projectName,
                testcaseNum: testcaseNum,
                imgName: imgName,
                question: discussText,
                model_id: mID
            };
            var actionurl = "createNewDiscussion";
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
                    console.log(response.discuss_id)
                    var fullDiscussURL = discussURL + "&discuss_id=" + response.discuss_id;
                    window.location.href = fullDiscussURL;

                },
                error: (function (jqXHR, textStatus, errorThrown) {
                    alert(jqXHR.status + textStatus + errorThrown);
                    //window.location.replace('404.html')
                })

            });
            //window.location.href = discussURL;
        }
    });

}
