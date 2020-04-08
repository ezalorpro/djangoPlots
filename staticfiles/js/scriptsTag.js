$(document).ready(function () {
    
    $('#id_formaPlots').submit(function (e) {
        e.preventDefault()
        $.ajax({
            url: url_resultsplot,
            type: 'post',
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'x_points': $("#id_x_points").val(),
                'y_points': $("#id_y_points").val()
            },
            success: function (data) {
                $('#plot-content').html(data);
            }
        });
    });

    // Validación dinámica usuario
    $('#id_username').on('input', function (e) {
        var valor = $('#id_username').val();
        console.log(String(valor).length);
        if (valor.length > 0) {
            e.preventDefault();
            $.ajax({
                url: url_registrar,
                type: 'get',
                data: {
                    name: $('#id_username').val(),
                },
                success: function (data) {
                    if (data.flag) {
                        $('#user_exist').css('display', 'block');
                        $('#user_error').css('display', 'none');
                        $('#user_avilable').css('display', 'none');
                        document.getElementById("btnRegistrar").disabled = true;
                    } else {
                        $('#user_avilable').css('display', 'block');
                        $('#user_error').css('display', 'none');
                        $('#user_exist').css('display', 'none');
                        document.getElementById("btnRegistrar").disabled = false;
                    }
                }
            });
        } else {
            $('#user_exist').css('display', 'none');
            $('#user_avilable').css('display', 'none');
            document.getElementById("btnRegistrar").disabled = true;
        };
    });

    // Validación dinámica email
});