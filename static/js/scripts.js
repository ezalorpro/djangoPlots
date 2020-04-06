$(document).ready(function () {
    
    // Inicializacion de los componentes de Materializecss
    M.AutoInit();
    
    // Para los el menu
    $('.dropdown-trigger').dropdown({
        constrainWidth: false
    });
    
    $('select').formSelect();

    //  Para actualizar la imagen seleccionada en el avatar del perfil
    $("#id_avatar").change(function () {
        readURL(this);
    });

    // Para el carousel del homepage
    $('.carousel.carousel-slider').carousel({
        fullWidth: true,
        indicators: true
    });

    $('.modal').modal();
    
});

//  Para actualizar la imagen seleccionada en el avatar del perfil
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#imgEdit').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
};