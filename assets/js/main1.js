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

// document.addEventListener("DOMContentLoaded", function () {
//     const overlay = document.getElementById('overlay');
//     const closeBtn = document.getElementById('closeBtn');

//     function openPopup() {
//         overlay.style.display = 'block';
//     }

//     function closePopup() {
//         overlay.style.display = 'none';
//     }

//     closeBtn.addEventListener('click', closePopup);
//     window.addEventListener('click', function (event) {
//         if (event.target === overlay) {
//             closePopup();
//         }
//     });

//     // Check if popup has already been displayed in this session
//     const popupDisplayed = getCookie('popupDisplayed');
//     if (!popupDisplayed) {
//         // Popup has not been displayed yet in this session, so open it
//         openPopup();
//         // Set flag in cookies to indicate that popup has been displayed
//         setCookie('popupDisplayed', 'true', 365); // Cookie expires in 365 days
//     } else {
//         // Popup has already been displayed, so don't open it again
//         closePopup();
//     }

//     // You can add form submission functionality here using AJAX or other methods
//     const registerForm = document.getElementById('registerForm');
//     registerForm.addEventListener('submit', function (event) {
//         event.preventDefault();
//         // Example: you can handle form submission here
//         console.log('Form submitted');
//         closePopup();
//     });
// });

// function setCookie(name, value, days) {
//     const date = new Date();
//     date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
//     const expires = "expires=" + date.toUTCString();
//     document.cookie = name + "=" + value + ";" + expires + ";path=/";
// }

// function getCookie(name) {
//     const decodedCookie = decodeURIComponent(document.cookie);
//     const cookies = decodedCookie.split(';');
//     for (let i = 0; i < cookies.length; i++) {
//         let cookie = cookies[i];
//         while (cookie.charAt(0) === ' ') {
//             cookie = cookie.substring(1);
//         }
//         if (cookie.indexOf(name) === 0) {
//             return cookie.substring(name.length + 1, cookie.length);
//         }
//     }
//     return "";
// }

// $(document).ready(function () {
//     $("#studentRegisterBtn").click(function (e) {
//         e.preventDefault(); 
//         $("#register").fadeIn(); 
//     });

//     $("#closeBtn").click(function () {
//         $("#register").fadeOut(); 
//     });
// });

// $(document).ready(function () {
//     $("#branchRegisterBtn").click(function (e) {
//         e.preventDefault(); 
//         $("#branch").fadeIn(); 
//     });

//     $("#closeBtn").click(function () {
//         $("#branch").fadeOut(); 
//     });
// });

// $(document).ready(function () {
//     $("#branchRegisterBtn").click(function (e) {
//         e.preventDefault(); 
//         $("#branch").fadeIn(); 
//     });

//     $("#studentRegisterBtn").click(function (e) {
//         e.preventDefault(); 
//         $("#register").fadeIn(); 
//     });

//     $("#closeBtn, #closeFormBtn").click(function () {
//         $("#branch, #register").fadeOut(); 
//     });
// });

// Auto scroll the carousel infinitely
$(document).ready(function () {
    $('#course-carousel').carousel({
        interval: 3000, // Change interval as needed
        wrap: true // Set to true for infinite scrolling
    });
});

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
