$(document).ready(function () {
    
    M.AutoInit();
    
    $('.dropdown-trigger').dropdown({
        constrainWidth: false
    });
    
    $('select').formSelect();

    $("#id_avatar").change(function () {
        readURL(this);
    });

    $('.carousel.carousel-slider').carousel({
        fullWidth: true,
        indicators: true
    });

    $('.modal').modal();

});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#imgEdit').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
};