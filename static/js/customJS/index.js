
$(document).ready(function () {
    $('#explore').click(function(e){
        e.preventDefault();
        var jumpId = $(this).attr('href');
        $('body, html').animate({scrollTop: $(jumpId).offset().top}, 'slow');
    });
    _init();
});
function _init(){
    //Click Listener for each category
    $(".feature_item").click(function() {
        location.href= "./category.html"
    });
}
