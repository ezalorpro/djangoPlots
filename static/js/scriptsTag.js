$(document).ready(function () {
    
    // Plot de data con Ajax
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
    $('#id_username').on('input', function (en) {
        user_validacion(en);
        flag3 = password1_validacion(en);
    });

    // Validación dinámica de email
    $('#id_email').on('input', function (en) {
        email_validacion(en);
        flag3 = password1_validacion(en);
    });

    $('#id_first_name').on('input', function (en) {
        flag3 = password1_validacion(en);
        habilitar_boton(en);
    });

    $('#id_last_name').on('input', function (en) {
        flag3 = password1_validacion(en);
        habilitar_boton(en);
    });

    // Validación dinámica del password
    $('#id_password1').on('input', function (en) {
        flag3 = password1_validacion(en);
        flag4 = password2_validacion(en);
        habilitar_boton(en);
    });
    $('#id_password2').on('input', function (en) {
        flag4 = password2_validacion(en);
        habilitar_boton(en);
    });

    // Función para validación dinámica de usuario
    function user_validacion(e) {
        var valor = $('#id_username').val();
        var flag = false;
        if (valor.length > 0) {
            e.preventDefault();
            $.ajax({
                url: url_registrar,
                type: 'get',
                data: {
                    name: $('#id_username').val(),
                    tipo: 'username',
                },
                success: function (data) {
                    if (data.flag) {
                        $("#user_exist").attr('class', 'invalido');
                        $("#user_exist").html('<i class="material-icons">cancel</i> Nombre de usuario ya existe, intente con otro');
                        flag1 = false;
                    } else {
                        $("#user_exist").attr('class', 'valido');
                        $("#user_exist").html('<i class="material-icons">check_circle</i> Nombre de usuario disponible');
                        flag1 = true;
                    }
                    habilitar_boton(e);
                }
            });
        } else {
            $("#user_exist").attr('class', 'valido');
            $("#user_exist").html('<i class="material-icons">info_outline</i> Ingrese un nombre de usuario');
            return flag
        };
    };

    // Función para validación dinámica de email
    function email_validacion(e) {
        var valor = $('#id_email').val();
        var flag = false;
        if (valor.length > 0) {
            e.preventDefault();
            $.ajax({
                url: url_registrar,
                type: 'get',
                data: {
                    email: $('#id_email').val(),
                    tipo: 'email',
                },
                success: function (data) {
                    if (data.flag) {
                        $("#email_validation").attr('class', 'valido');
                        $("#email_validation").html('<i class="material-icons">check_circle</i> Correo electrónico valido');
                        flag2 = true;
                    } else {
                        $("#email_validation").attr('class', 'invalido');
                        $("#email_validation").html('<i class="material-icons">check_circle</i> ' + data.info);
                        flag2 = false;
                    }
                    habilitar_boton(e);
                }
            });
        } else {
            return flag
        };
    };

    function password1_validacion(e) {
        var valor = $('#id_password1').val();
        var flag_1 = false;
        var flag_2 = false;
        var flag_3 = false;
        if (valor.length > 0) {

            if (valor.length > 7) {
                $("#password11_validation").attr('class', 'valido');
                $("#password11_validation").html('<i class="material-icons">check_circle</i> La contraseña debe contener al menos 8 caracteres.');
                flag_1 = true;
            } else {
                $("#password11_validation").attr('class', 'invalido');
                $("#password11_validation").html('<i class="material-icons">cancel</i> La contraseña debe contener al menos 8 caracteres.');
                flag_1 = false;
            }

            var total = (new RegExp('[a-z]')).test(valor) + (new RegExp('[A-Z]')).test(valor) + (new RegExp('[1-9]')).test(valor) + (new RegExp('[$@$!%*#?&]')).test(valor);

            if (total > 1) {
                $("#password12_validation").attr('class', 'valido');
                $("#password12_validation").html('<i class="material-icons">check_circle</i> La contraseña no puede ser demasiado común.');
                flag_2 = true;
            } else {
                $("#password12_validation").attr('class', 'invalido');
                $("#password12_validation").html('<i class="material-icons">cancel</i> La contraseña no puede ser demasiado común.');
                flag_2 = false;
            }

            difflib['SequenceMatcher'](valor, $('#id_username').val());
            var comp_username = difflib.ratio()
            
            difflib['SequenceMatcher'](valor, $('#id_email').val());
            var comp_email = difflib.ratio()
            
            difflib['SequenceMatcher'](valor, $('#id_first_name').val());
            var comp_first = difflib.ratio()
            
            difflib['SequenceMatcher'](valor, $('#id_last_name').val());
            var comp_last       = difflib.ratio()

            max_comp = Math.max(comp_username, comp_email, comp_first, comp_last)

            if (max_comp < 0.60) {
                $("#password13_validation").attr('class', 'valido');
                $("#password13_validation").html('<i class="material-icons">check_circle</i> La contraseña no debe coincidir con tus datos personales.');
                flag_3 = true;
            } else {
                $("#password13_validation").attr('class', 'invalido');
                $("#password13_validation").html('<i class="material-icons">cancel</i> La contraseña no debe coincidir con tus datos personales.');
                flag_3 = false;
            }
            
            if (flag_1 && flag_2 && flag_3) {
                return true
            } else {
                return false
            }
        } else {
            return false
        };
    };

    function password2_validacion(e) {
        var valor1 = $('#id_password1').val();
        var valor2 = $('#id_password2').val();
        var flag = false;
        if (valor2.length > 0 || valor1.length > 0) {

            if (valor1 === valor2) {
                $("#password2_validation").attr('class', 'valido');
                $("#password2_validation").html('<i class="material-icons">check_circle</i> Ambas contraseñas deben coincidir.');
                flag = true;
            } else {
                $("#password2_validation").attr('class', 'invalido');
                $("#password2_validation").html('<i class="material-icons">cancel</i> Ambas contraseñas deben coincidir.');
                flag = false;
            }
            return flag
        } else {
            return flag
        };
    };

    function habilitar_boton(e) {
        if (flag1*flag2*flag3*flag4) {
            document.getElementById("btnRegistrar").disabled = false;
        } else {
            document.getElementById("btnRegistrar").disabled = true;
        }
    }
});