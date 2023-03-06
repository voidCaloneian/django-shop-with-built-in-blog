
function visual_update(value){
    widget = $('.header__cart__price span')[0]
    widget.innerText = `${value} ₽` 
}

function refresh_shopping_cart_widget_balance(){
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/shop/shopping_cart_get_total_price/',
        data:separator(getCookie('product_ids')),
        success: function(data){
            visual_update(data['total_price'])}
    })
}

// Обновляет количество виджета 'Корзина'
function refreshCartWidgetCounter(){
    let new_value = Object.keys(separator()).length
    if (new_value){
        $('.refreshCartWidgetCounter')[0].innerText = new_value
    } else {
        $('.refreshCartWidgetCounter')[0].innerText = 0
    }
}
