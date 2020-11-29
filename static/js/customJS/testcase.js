var projectName;
var testCaseNum;
var model_id;
var discuss_id;
/*Firebase Storage Implementation*/
var firebaseConfig = {
    apiKey: "AIzaSyAz7DBKf9tXXevwGIb08IJLwGC4vSlAir0",
    authDomain: "cs5597-directed-reading.firebaseapp.com",
    databaseURL: "https://cs5597-directed-reading.firebaseio.com",
    projectId: "cs5597-directed-reading",
    storageBucket: "cs5597-directed-reading.appspot.com",
    messagingSenderId: "172359783153"
};

// Get a reference to the storage service, which is used to create references in your storage bucket
// Firebase App is always required and must be first
firebase.initializeApp(firebaseConfig);
var storage = firebase.storage();
var defaultImgRef = storage.ref('user-profile-images/user.png');
var imageRef = storage.ref('user-profile-images');
var storageRef = storage.ref();
/*********************************/
$(document).ready(function () {
    function loadImage(pName, tName, imgName){
        $('#previewImg').attr('src', './tmp/' + pName + '/' + tName + '/' + imgName);
    }
    function loadChart(pName, tName){
        var response = [];
        jQuery.get('./tmp/' + pName + '/' + tName + '/predictions.txt', function(data) {
            var myvar = data;
            console.log(data);
            var str = data.toString();
            str = str.substr(1,str.length-2);
            var result = str.split(", ");

            console.log(result);
            for (i=0;i<result.length;i+=2)
            {
                //console.log(res[i][res[i].length-2] + res[i][res[i].length-1]);
                result[i]=result[i].substr(2,result[i].length-3);
                result[i+1] = result[i+1].substr(0,result[i+1].length-1);
                console.log(result[i]);
                console.log(result[i+1]);
                response.push({"classname" : result[i],
                        "value": result[i+1]
                    }
                )
            }
            /////Chart Rendering
            var chartData =[], xAxis = [];
            for (i=0;i<response.length;i++){
                chartData.push(response[i].value * 100);
                xAxis.push(response[i].classname);
            }
            console.log(chartData);
            console.log(xAxis);

            ///Chart Section
            var chartHeight=130 + 40* response.length;
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
                        return val.toFixed(2)
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
                    text: 'Model: ' + pName,
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
        });


    }
    function getTestCaseInfo(info_obj){
        console.log("in getTestCaseDiscussionInfo()");
        var data = info_obj;
        console.log(data);
        var actionurl = "getTestCaseDiscussionInfo";
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
                updateUI(response);

            },
            error: (function (jqXHR, textStatus, errorThrown) {
                alert(jqXHR.status + textStatus + errorThrown);
                //window.location.replace('404.html')
            })

        });

    }
    function updateUI(response){
        updateProfileImage($(".owner-avatar"), response.owner_profile_url);
        $(".owner-name").text(response.owner);
        $(".thread-date").text(response.create_date);
        $(".thread-text").text(response.question);
        $(".total-comment-num").text(response.comments.length);
        //Comment Section

        if (response.comments.length == 0){
            var text = "BE THE FIRST TO COMMENT ON THIS POST!"
            $(".comment-notification-text").text(text);
            $(".comment-notification-text").show();
        }
        else {
            $(".comment-notification-text").hide();
            for (var i = 0; i < response.comments.length; i++ ){
                var commentOwner = response.comments[i].name;
                var commentDate = response.comments[i].date;
                var commentText = response.comments[i].text;
                var profileImgURL = response.comments[i].profile_img_url;
                var newCommentItem = $('#comment-item').clone();
                newCommentItem.attr("id", "comment-item-" + i);
                newCommentItem.show();
                $("#comment-board").append(newCommentItem);

                var currentItemID = "#comment-item-" + i;


                $(currentItemID +  " .commenter-name").text(commentOwner);
                $(currentItemID +  " .comment-date").text(commentDate);
                $(currentItemID + " .comment-text").text(commentText);


                var avatar = $(currentItemID + " .commenter-avatar");

                updateProfileImage(avatar, profileImgURL );

            }



        }
    }
    function updateProfileImage(item,URL){
        console.log("in updateProfileImage");
        console.log(item);
        imageRef.child(URL).getDownloadURL().then(function(url) {
            // `url` is the download URL for 'images/stars.jpg'
            console.log(url);
            // Or inserted into an <img> element:
            item.attr("src", url);
        }).catch(function(error) {
            // Handle any errors
        });
    }
    function listenToUserComment(){
        $("#comment-submit").click(function(){
            var text = $("#comment-text-area").val();
            var data = {
                testcaseNum: testcaseNum,
                model_id: model_id,
                text: text,
                name: username,
                user_id: user_id,
                date: getCurrentDate(),
                discuss_id: discuss_id,
            };
            console.log(data);
            var actionurl = "saveNewComment";
            $.ajax({
                url: actionurl,
                cache: false,
                contentType: "application/json; charset=utf-8",
                processData: false,
                method: 'POST',
                dataType: 'text',
                data: JSON.stringify(data),
                success: function (response, status, jqXHR) {
                    console.log('in success ' + jqXHR.status);
                    console.log(response);
                    var text = "YOUR COMMENT HAS BEEN POSTED! THANK YOU FOR YOU CONTRIBUTION!"
                    $(".comment-notification-text").text(text);
                    $(".comment-notification-text").show();
                    $("#comment-text-area").val("");

                },
                error: (function (jqXHR, textStatus, errorThrown) {
                    alert(jqXHR.status + textStatus + errorThrown);
                    $(".comment-notification-text").hide();
                    $("#comment-text-area").val("");
                    //window.location.replace('404.html')
                })

            });
        })


    }

    function getCurrentDate(){
        //Function to get current date
        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var yyyy = today.getFullYear();
        /////////////////////////////////////////////////////////

        today = mm + '/' + dd + '/' + yyyy;
        return today;
    }
    function init(){
        //Hide Default Comment;
        $("#comment-item").hide();


        fullURL = window.location.href;
        var url = new URL(fullURL);
        projectName = url.searchParams.get("id");
        testcaseNum = url.searchParams.get("testid");
        var imgName = url.searchParams.get("imgname");
        model_id = url.searchParams.get("m_id");
        discuss_id = url.searchParams.get("discuss_id");
        var info_obj = {
            url : url,
            projectName : projectName,
            testcaseNum : testcaseNum,
            imgName : imgName,
            model_id: model_id,
            discuss_id: discuss_id
        };
        $("#testnum").text(testcaseNum);
        $("#projectname").text(projectName);
        loadImage(projectName, testcaseNum, imgName);
        loadChart(projectName, testcaseNum);
        getTestCaseInfo(info_obj);
        listenToUserComment();

    }
    init();
});