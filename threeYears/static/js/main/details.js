var last_review_index = 4
// Функция, работающая на странице 'Товар в Деталях', 
//   которая получает количество выбранного товара
function getAmountFromDetails(item){
    return $(item).parent().find('input').val()
}

// Нажатие на надпись 'Отзывы({n})' скрывает, либо раскрывает блок отзывов
function hideReviews(){
    // Функция ставит параметр стиля 'display' на противоположный,
    // обращая внимание на текущий класс, класс меняется после смены стиля
    let panel = $('.product__details__tab__desc')
    let classes = panel[0].className
    if (classes == 'product__details__tab__desc'){
        panel.css({'display' : 'block'})
        panel[0].className = 'product__details__tab__desc active'
    } else{
        panel.css({'display' : 'none'})
        panel[0].className = 'product__details__tab__desc'
    }
    
}

// Функция смены состояния кнопки со страницы "Товар в деталях"
function swapButtonColor(force = false){
    let button = document.getElementsByClassName('primary-btn')[0]
    let classes = button.className
    let quantity = $('div .quantity')[0]

    if (classes == 'primary-btn primary-btn-added' && !force){
            button.className = 'primary-btn'
            button.innerText = 'Добавить в Корзину'
            quantity.className = 'quantity'
    } else {
        button.className = 'primary-btn primary-btn-added'
        button.innerText = 'Убрать из Корзины'
        quantity.className = 'quantity active'
    }
}

function getProductId(){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    return urlParams.get('id');
}

if (document.getElementsByClassName('primary-btn')[0].className == 'primary-btn primary-btn-added'){
    let quantity = $('div .quantity')[0]
    quantity.className = 'quantity active'

    let productId = getProductId()

    $('div .quantity input')[0].value = separator()[parseInt(productId)]
}

get_more_review_button = $('#get_more_review')[0]

function insertNewReviews(reviews){
    let previousElement = document.querySelector('.row.my-3.p-3:last-of-type');
    previousElement.insertAdjacentHTML('afterend', reviews);
}

get_more_review_button.onclick = () =>{
    $.ajax({
        type:'GET',
        url:'/shop/review/get_more/',
        data:{
            'product_id':getProductId(),
            'last_review_index' : last_review_index
        },
        success: function(data){
            insertNewReviews(data['reviews'])
            last_review_index += 4
        }
    })
}

function postReviewChanges(review){
    
    // Убираем форму добавления отзыва
    $("#post_review_div").remove();
    // Визуально добавляем наш отзыв 
    review_tab = $('.product__details__tab__desc')[0]
    review_tab.insertAdjacentHTML('afterbegin', review)
    // Добавляем к визуальному количеству отзывов единичку
    reviews_counter = $('.product__details__label')[0]
    reviews_counter.innerText = `Отзывы (${parseInt($(reviews_counter).data('value')) + 1})`
    
}

function makeHtmlReviewBlock(text, rating){
    return `<div class="row my-3 p-3" style="background-color: #F0F6FFA1;">
                <div class="col-md-12">
                    <div class="media">
                        <div class="media-body">
                            <h6 class="mt-0 d-inline">Ваш отзыв</h6>
                            <p class="d-inline ml-3 mb-0">Оценка - <span class="badge badge-secondary">${rating}</span></p>
                            <p>${text}</p>
                        </div>
                    </div>
                </div>
            </div>
           `
}

var review 
var rating

function postReview(){
    review = $('#review_text')[0].value
    rating = $('#review_rating')[0].value
    $.ajax({
    type:'POST',
    url:'/shop/review/',
    data:{
        'product_id':getProductId(),
        'review': review,
        'rating': rating
    }, headers: {'X-CSRFToken' : getCookie('csrftoken')},
    success: function(){
        postReviewChanges(makeHtmlReviewBlock(review, rating))
    }
})
}

// Функция смены цвета добавления товара в корзину на странице каталога (с белого на зеленый и наоборот)
function changeCartColor(item){
    if (item.className == ''){
        item.className = 'fa-shopping-cart-added'
    } else{
        item.className = ''
    }
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
}