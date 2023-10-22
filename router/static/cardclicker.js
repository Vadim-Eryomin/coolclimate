function changeShop() {
    let sel = $('#variant').val()
    $('.variant').addClass('d-none')
    $(`.variant#${sel}`).removeClass('d-none');
    console.log(sel);
}