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

const RegisterBtnClick = async function () {
    data = new FormData();
    data.append("username", document.getElementById("username").value);
    data.append("email", document.getElementById("email").value);
    data.append("password", document.getElementById("password").value);
    data.append("confirmpassword", document.getElementById("confirmpassword").value);
    data.append("residential_address", document.getElementById("residential_address").value);
    data.append("dob", document.getElementById("dob").value);
    data.append("father_name", document.getElementById("father_name").value);
    data.append("branch", document.getElementById("branch").value);
    data.append("course", document.getElementById("course").value);
    const resp = await axios.post("/register/", data);
    alert(resp.data.message);
    if (resp.data.message === "OTP sent to your email. Please verify.") {
        window.location.href = "/login/";
    }
};

const LoginBtnClick = async function () {
    data = new FormData();
    data.append("email", document.getElementById("email").value);
    data.append("password", document.getElementById("password").value);
    var resp = await axios.post("", data);
    alert(resp.data.message);
    // if (resp.data.message === "Login successful") {
    //     location.href = "/dashboard/?data=" + resp.data.user_id;
    // }
};