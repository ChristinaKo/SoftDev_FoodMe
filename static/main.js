$(document).ready(function () {

    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.scrollup').fadeIn();
        } else {
            $('.scrollup').fadeOut();
        }
    });

    $('.scrollup').click(function () {
        $("html, body").animate({
            scrollTop: 0
        }, 600);
        return false;
    });

    $('.trigger').click(function (){
	$(".trigger").not(this).next(".toggle-e").slideUp("slow");
    $(this).next(".toggle-e").slideToggle("slow");

    })

});
