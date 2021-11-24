// username checker



$(document).ready(function () {
    $("#username-input").keyup(function () {
        var username = $(this).val();
        console.log(username);
        if (username != "") {
            $.ajax({
                url: '/username/',
                type: 'POST',
                data: { username: username }
            }).done(function (response) {
                console.log(response);
                if (response == "False") {
                    if ($("#username-checker").hasClass('fa-check-circle')) {
                        $('#username-checker').removeClass('fa-check-circle')
                    }
                    $('#username-checker').addClass('fa-times-circle')
                }
                else if (response == "True") {
                    if ($("#username-checker").hasClass('fa-times-circle')) {
                        $('#username-checker').removeClass('fa-times-circle')
                    }
                    $('#username-checker').addClass('fa-check-circle')
                }
                else {
                    if ($("#username-checker").hasClass('fa-check-circle')) {
                        $('#username-checker').removeClass('fa-check-circle')
                    }
                    if ($("#username-checker").hasClass('fa-times-circle')) {
                        $('#username-checker').removeClass('fa-times-circle')
                    }
                
                }
            })
                .fail(function () {
                    console.log("failed");
                })
        }
        else{
            if ($("#username-checker").hasClass('fa-check-circle')) {
                $('#username-checker').removeClass('fa-check-circle')
            }
            if ($("#username-checker").hasClass('fa-times-circle')) {
                $('#username-checker').removeClass('fa-times-circle')
            }
        }
    });
})


/**
 * add correct icon if username is available
 */
function usernameStatus(id) {
    var username = $(`#${id}`).val();
    console.log(username);
    if (username != "") {
        $.ajax({
            url: '/username/',
            type: 'POST',
            data: { username: username }
        }).done(function (response) {
            // console.log(response);
            if (response == "False") {
                if ($("#username-checker").hasClass('fa-check-circle')) {
                    $('#username-checker').removeClass('fa-check-circle')
                }
                $('#username-checker').addClass('fa-times-circle')
            }
            else if (response == "True") {
                if ($("#username-checker").hasClass('fa-times-circle')) {
                    $('#username-checker').removeClass('fa-times-circle')
                }
                $('#username-checker').addClass('fa-check-circle')
            }
            else {
                if ($("#username-checker").hasClass('fa-check-circle')) {
                    $('#username-checker').removeClass('fa-check-circle')
                }
                if ($("#username-checker").hasClass('fa-times-circle')) {
                    $('#username-checker').removeClass('fa-times-circle')
                }

            }
        })
            .fail(function () {
                console.log("failed");
            })
    }
}



/**
 * add correct if email is available
 */
function emailStatus(id) {
    var email = $(`#${id}`).val();

    if (email != "") {
        $.ajax({
            url: '/email/',
            type: 'POST',
            data: { email: email }
        }).done(function (response) {
            // console.log(response);
            if (response == "False") {
                if ($("#email-checker").hasClass('fa-check-circle')) {
                    $('#email-checker').removeClass('fa-check-circle')
                }
                $('#email-checker').addClass('fa-times-circle')
            }
            else if (response == "True") {
                if ($("#email-checker").hasClass('fa-times-circle')) {
                    $('#email-checker').removeClass('fa-times-circle')
                }
                $('#email-checker').addClass('fa-check-circle')
            }
            else {
                if ($("#email-checker").hasClass('fa-check-circle')) {
                    $('#email-checker').removeClass('fa-check-circle')
                }
                if ($("#email-checker").hasClass('fa-times-circle')) {
                    $('#email-checker').removeClass('fa-times-circle')
                }

            }
        })
            .fail(function () {
                console.log("failed");
            })
    }
}