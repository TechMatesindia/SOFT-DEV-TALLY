(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();


    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.sticky-top').addClass('shadow-sm').css('top', '0px');
        } else {
            $('.sticky-top').removeClass('shadow-sm').css('top', '-100px');
        }
    });


    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
        return false;
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        items: 1,
        dots: true,
        loop: true,
    });


})(jQuery);
document.addEventListener("DOMContentLoaded", function () {
    const overlay = document.getElementById('overlay');
    const closeBtn = document.getElementById('closeBtn');

    function openPopup() {
        overlay.style.display = 'block';
    }

    function closePopup() {
        overlay.style.display = 'none';
    }

    closeBtn.addEventListener('click', closePopup);
    window.addEventListener('click', function (event) {
        if (event.target === overlay) {
            closePopup();
        }
    });

    // Automatically open the popup on page load
    openPopup();

    // You can add form submission functionality here using AJAX or other methods
    const registerForm = document.getElementById('registerForm');
    registerForm.addEventListener('submit', function (event) {
        event.preventDefault();
        // Example: you can handle form submission here
        console.log('Form submitted');
        closePopup();
    });
});
$(document).ready(function () {
    $("#studentRegisterBtn").click(function (e) {
        e.preventDefault(); // Prevent default form submission
        $("#register").fadeIn(); // Show the registration pop-up
    });

    $("#closeBtn").click(function () {
        $("#register").fadeOut(); // Close the registration pop-up when close button is clicked
    });
});

$(document).ready(function () {
    $("#branchRegisterBtn").click(function (e) {
        e.preventDefault(); // Prevent default form submission
        $("#branch").fadeIn(); // Show the registration pop-up
    });

    $("#closeBtn").click(function () {
        $("#branch").fadeOut(); // Close the registration pop-up when close button is clicked
    });
});
$(document).ready(function () {
    $("#branchRegisterBtn").click(function (e) {
        e.preventDefault(); // Prevent default form submission
        $("#branch").fadeIn(); // Show the registration pop-up
    });

    $("#studentRegisterBtn").click(function (e) {
        e.preventDefault(); // Prevent default form submission
        $("#register").fadeIn(); // Show the registration pop-up
    });

    $("#closeBtn, #closeFormBtn").click(function () {
        $("#branch").fadeOut(); // Close the registration pop-up when close button is clicked
    });
    $("#closeBtn, #closeFormBtn").click(function () {
        $("#register").fadeOut(); // Close the registration pop-up when close button is clicked
    });
});


// Auto scroll the carousel infinitely
$(document).ready(function () {
    $('#course-carousel').carousel({
        interval: 3000, // Change interval as needed
        wrap: true // Set to true for infinite scrolling
    });
});

//  $(document).ready(function(){
//         $('#course-carousel').owlCarousel({
//             items: 3,
//             loop: true,
//             autoplay: true,
//             autoplayTimeout: 2000 // Change autoplay timeout as needed
//         });
//     });

let valueDisplays = document.querySelectorAll(".num");
let interval = 4000;

valueDisplays.forEach((valueDisplay) => {
    let startValue = 0;
    let endValue = parseInt(valueDisplay.getAttribute("data-val"));
    let duration = Math.floor(interval / endValue);
    let counter = setInterval(function () {
        startValue += 1;
        valueDisplay.textContent = startValue;
        if (startValue == endValue) {
            clearInterval(counter);
        }
    }, duration);
});

$(document).ready(function () {
    $("#addBranchBtn").click(function (e) {
        e.preventDefault(); 
        $("#branch").fadeIn(); 
    });
});