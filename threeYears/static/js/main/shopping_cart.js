
var input = document.getElementsByClassName('promoInput')[0]
var button = document.getElementsByClassName('promoButton')[0]
var p = document.getElementsByClassName('promoP')[0]

function switchPromoPStyle(show){
    if (show){
        p.classList = 'promoP show'
    } else{
        p.classList = 'promoP hide'
    }
}

var promo_is_active = false

if (button){
    button.addEventListener('click', () => {
        promo = input.value
        if (!promo_is_active){
            $.ajax({
                type: 'GET',
                url : '/shop/promo/',
                data:{
                    'promo': promo
                }, success: function(data){
                    activateOrCancelPromo(activate=true, data)
                    refreshTotalPriceUsingPromo(data['discount'])
                } 
            })
        } else{
            activateOrCancelPromo(activate=false)
            refreshTotalPriceUsingPromo(0)
        }
    })
}

function activateOrCancelPromo(activate, data = null){
    if (activate){
        switchPromoButtonStyle(data, active=true)
        switchPromoPStyle(show=true)
        promo_is_active = true
    } else{
        switchPromoButtonStyle(data=null, active=false)
        switchPromoPStyle(show=false)
        promo_is_active = false
    }
}

function switchPromoButtonStyle(data = null, active = true){
    if (active){
        $('.promoBeta')[0].innerText = data['description'] 
        $('.promoBeta')[1].innerText = data['discount'] + '%'
        button.classList.add('promoButtonActive')
        button.innerHTML = 'Отменить'
    } else{
        button.classList.remove('promoButtonActive')
        button.innerHTML = 'Применить'
    }
}

// Функция устанавливает соответствующие значения аргумента 'value', которое играет роль " количество_товара " в коде 
function refreshProductsAmount(){
    // Количественный блок имеет класс " setMyValues ", по элементам этого класса мы и проходим
    $('.setMyValues').each(function(){
        let product_id = $(this).data('product_id')
        let amount = separator()[product_id]
        this.value = amount
    })
}
        // Функция, отвечающая за финальную цену продукта (с учётом его количества)
function changeProductTotalPrice(item = null, newVal = null){
    refreshProductsAmount()
    function __changeIt(item, newVal){
        // Визуальное обновление
        let parents = $(item).parent().parent().parent().parent()
        let price = parseInt(parents.find('.shoping__cart__onPrice').text())
        parents.find('.shoping__cart__total').text(`${parseInt(newVal) * price} ₽`)
    }

    // item == null на загрузке страницы, чтобы установить товарам цены, соответствующие формуле " цена_товара * количество_товара "
    if (item == null){
        $('.setMyValues').each(function(){
            let value = $(this).val()
            __changeIt(this, value)
        })
    // Выполняется, когда происходит смена количества товара
    }else{
        __changeIt(item, newVal)
    }
}


// Функция вызывается, когда удаляемый товар оказывается последним
function removeContentIfLastProductInShoppingCart(product_in_html){
    // Удаление html блоков кода, в которых отображалась таблица продуктов и общая цена корзины
    product_in_html.parentNode.parentNode.remove()
    $('.shoping__continue')[0].parentNode.remove()
    $('.shoping__checkout')[0].parentNode.remove()
    
    // Добавление поверх оставшихся эллементов надписи
    let table = $('.shoping__cart__table')[0]
    let code = '<center><h4 id="no__products_error">Вы ещё не добавили продуктов в вашу корзину!</h4></center>'
    table.insertAdjacentHTML('afterbegin', code)
    
}

// Функция визуального удаления товара со страницы корзины
function removeProductInHtml(id, array_length){
    let product_in_html = document.querySelector(`tr td[product_id='${id}']`).parentNode
    if (array_length == 1){removeContentIfLastProductInShoppingCart(product_in_html)} 
    
    product_in_html.remove()

}

// Функция, обновляющая общую цену корзины
function refreshTotalPrice(){

    // Визуальное изменение общей цены корзины
    function refreshTotalPriceVisualisation(total_price){
        
        let before_price_label = $('#beforeTotalPrice')
        before_price_label.text(`${total_price} ₽`)
        if (last_used_discount != 0){
            refreshTotalPriceUsingPromo(last_used_discount)
        } else {
            let after_price_label = $('#afterTotalPrice')
            after_price_label.text(`${total_price} ₽`)
        }
        
    }

    // Список всех продуктов
    let items = $('.shoping__cart__total')
    let total_price = 0
    // Сумма финальной цены каждого из продуктов
    for (var i = 0; i < items.length; i++) {
        total_price += parseInt(items[i].innerText)
    }
    
    refreshTotalPriceVisualisation(total_price)
}

var last_used_discount = 0
function refreshTotalPriceUsingPromo(discount){
    
    discount = parseInt(discount)

    let price_label = $('#afterTotalPrice')
    let normal_price_label = $('#beforeTotalPrice')

    let normal_price = parseInt(normal_price_label.text())
    let new_price = Math.round(normal_price * (100 - discount) / 100)

    price_label.text(`${new_price} ₽`)
    last_used_discount = discount
}



changeProductTotalPrice()
refreshTotalPrice()