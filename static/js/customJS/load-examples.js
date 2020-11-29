$(document).ready(function () {
    var fullURL = window.location.href;
    var url = new URL(fullURL);
    var pName = url.searchParams.get("id");
    function loadImages(){
        var actionurl = "latest-cases";
        console.log('in client loadImages() ' + pName);
        var data = {};
        data.pname = pName;
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
                for (var i = 0; i < response.image.length; i++){
                    var newImg = $('#demo-' + i);
                    var newThumb = $('#demo-thumb-' + i);
                    newImg.find("img").attr('src', response.image[i].path);
                    newThumb.find("img").attr('src', response.image[i].path);
                    //newImg.find("h6").html('Date: ' + "<i>" + response.image[i].date.toString() + "</i>");
                    newImg.attr('id', response.image[i].name);
                    newThumb.attr('casename', response.image[i].name);
                    //newImg.show();
                    //$("#demo-container").append(newImg);
                }
                var response = [];
                $( ".carousel-thumbnails li").click(function() {
                    $("#chart").empty();
                    var response = [];
                    console.log("clicked " + $(this).attr("id"));
                    var tName = $(this).attr("casename");
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
                    $('.result').show();
                    $('#rating-btn').hide();
                    enableDiscussBtnListener("http://127.0.0.1:8080/discussion.html?id=EnlargenHeart&testid=testcase-1558044562577&imgname=xray.jpg&m_id=AeOxsBsMXGJCSDtez8Sj");
                });
            },
            error: (function (jqXHR, textStatus, errorThrown) {
                //alert(jqXHR.status + textStatus + errorThrown);
                window.location.replace('404.html')
            })

        });
    }

    function init(){
        $('#hidden-demo').hide();
        loadImages();
    }
    init();
});