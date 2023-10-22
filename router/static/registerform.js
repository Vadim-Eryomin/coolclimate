function submit(e) {
    if ($('#password1').val() != $('#password2').val()) {
        $('.alert').removeClass('d-none')
        e.stopPropagation();
        e.preventDefault();
    }
}

function change() {
    $('.alert').addClass('d-none')
}

onload = () =>
    form.onsubmit = e => submit(e)