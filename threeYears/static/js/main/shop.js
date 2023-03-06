// Функция смены цвета добавления товара в корзину на странице каталога (с белого на зеленый и наоборот)
function changeCartColor(item){
    if (item.className == ''){
        item.className = 'fa-shopping-cart-added'
    } else{
        item.className = ''
    }
}

// Обновляет значение 'Сортировать по',
// соответствующее текущему GET запросу при переходе на новую страницу пагинации
function refreshSortBy(){
    let translate = {
        null : 'Алфавиту', // Если в юрл GET параметрах нет параметра 'ordering'
        'Цена to-low' : 'Цена (по убыванию)',
        'Цена to-high' : 'Цена (по возрастанию)',
        'Алфавит' : 'Алфавиту',
        'Скидка' : 'Скидке' 
    }

    let sort_by_from_get_params = new URLSearchParams(window.location.search).get('ordering')
    let label = $('.current')[0]


    label.innerText = translate[sort_by_from_get_params]
}

function clearCookieSearchParams(){
    setCookie('params', '', 0)
}

// Функция выполняется после загрузки страницы, 
// чтобы изменить цвета картинок добавления товара в корзину, продукты которых в куках
function changeAllCartColor(){
    let cookies = getCookie('product_ids')

    // Проверка, есть ли продукты в корзине вообще
    if (cookies){
    
        cookies = cookies.split(' ') 
        let cookies_list = []
        
        // Создание листа, состоящего только из айди продуктов
        // Изначально лист состоит из элементов подобного стиля
        //               id_количествоТовара

        for (let i in cookies){
            let _id = cookies[i].split('_')[0]
            cookies_list.push(_id)
        }
        // Проход по каждому из товаров
        $('.fa-shopping-cart').each(function(){
            let item = this.parentNode
            let item_id = $(item).data('product_id').toString()
            if (cookies_list.includes(item_id)){
                item.className = 'fa-shopping-cart-added'
            } else{
                item.className = ''
            }
        })
    }
}3

changeAllCartColor()
updatePriceSlider()
refreshSortBy()
updateSortBy()
checkCookies()