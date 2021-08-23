/**
 * Owl initializer function
 */
$(document).ready(function(){
    $('.owl-carousel').owlCarousel({
        loop:true,
        margin:30,
        nav:true,
        navText:["<span class='carousel-nav-btn prev-slide'></span>","<span class='carousel-nav-btn next-slide'></span>"],
        responsive:{
            0:{
                items:1
            },
            600:{
                items:2
            },
            1000:{
                items:3
            }
        }
    });
});