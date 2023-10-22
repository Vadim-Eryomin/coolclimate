function plus(id) {
    value = +$('#quantity' + id).val()
    $('#quantity' + id).val(value + 1)
    recountSubtotal(id)
}

function minus(id) {
    value = +$('#quantity' + id).val() - 1
    value = value < 1 ? 1 : value
    $('#quantity' + id).val(value)
    recountSubtotal(id)
}

function recountSubtotal(id) {
    value = +$('#quantity' + id).val()
    cost = +$('#cost' + id).val()
    $('#subtotalvalue' + id).val((value * cost).toFixed(2))
    $('#subtotal' + id).text((value * cost).toFixed(2) + ' руб.')
    recount()
}

function recount() {
    let sum = 0
    $.each($("[id*='subtotalvalue']"), function (indexInArray, element) {
        sum += +$(element).val()
    });

    $('#total').text(sum.toFixed(2) + ' руб.')
}