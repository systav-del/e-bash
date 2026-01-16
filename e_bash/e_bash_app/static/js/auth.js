$('#auth-button').click(
    function() {
        let email = $('#email').val();
        let password = $('#password').val();
        let CSRF = $('[name=csrfmiddlewaretoken]').val();

        if (!email) {
            alert('введите адрес электронной почты!');
        }

        if (!password) {
            alert('введите пароль!');
        }

        let userData = {
            'email' : email,
            'password' : password,
            'csrfmiddlewaretoken' : CSRF
        }

        $.ajax({
            url: '/auth/',
            type: 'POST',
            dataType: 'json',
            data: userData,
            success: function(data) {
                window.location.href = '/';
            },
        });
    }
)