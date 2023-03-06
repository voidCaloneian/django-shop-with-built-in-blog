var search
var min_price
var max_price
var category
var ordering
var page

select = document.getElementById('select-sort-data')
slider = $('#slider')
// select.addEventListener('change', sendAjax) почему-то где-то ещё EventListener установлен уже

   
function getParamKeyViaUrl(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
};

function checkCookies(){
    if (getCookie('params')){
        if (getCookie('params').length <= 1){
            setCookie('params', `?category=${getParamKeyViaUrl('category')}&ordering=Алфавит`, 1)
        }
    } else{
        setCookie('params', `?category=${getParamKeyViaUrl('category')}&ordering=Алфавит`, 1)
    }
}

function setParamsCookies(){
    setCookie(
        'params', 
        `?category=${category}&ordering=${ordering}&min_price=${min_price}&max_price=${max_price}`,
        1
    )
}

function getData(){
    let prices = slider.slider('values')

    search = getParamKeyViaUrl('search')

    min_price = prices[0]
    max_price = prices[1]

    page = $('#current_page').data('value')
    if (page == '' || page == null){page = '1'}
    category = $('.product__discount__title h2')[0].innerText.toLowerCase()
   
    ordering = document.getElementById('select-sort-data').value

    setParamsCookies()
}

function validateCategory(category){
    if (category){return category}
    else{
        return 'акции'
    }
}

function sendAjax(){
    getData()
    setCookie('page', '1', 1)
    $.ajax({
        type:'GET',
        url :'http://127.0.0.1:8000/shop/',
        data: {
            'search' : search,
            'min_price' : min_price,
            'max_price' : max_price,
            'category'  : category,
            'ordering'  : ordering,
            'page'      : page
        },
        success: function(data){
            changeProductsBlock(data['products'])
            changePagination(data['pagination'])
            changeProductsAmount(data['products_amount'])
            refreshBackgrounds()
            setParamsCookies()
        }
    })
}

function changeProductsBlock(products){
    $('#product-wrapper').replaceWith(products);
}

function changePagination(pagination){
    $('#pagination-wrapper').replaceWith(pagination);
}

function changeProductsAmount(amount){
    $('#products_found').replaceWith(`<span id="products_found">${amount}</span>`);
}

function refreshBackgrounds(){
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css({'background-image' : 'url(' + bg + ')'});
    });
}

function setPage(item){
    setCookie('page', $(item).data('value'), 1)
}

function cookiesParamsDictionary(){
    let params = getCookie('params').slice(1).split('&')

    let paramsDictionary = {};
    for (let item of params) {
        let keyValue = item.split("=");
        paramsDictionary[keyValue[0]] = keyValue[1];
    }
    return paramsDictionary
}

function updatePriceSlider(){
    let params = cookiesParamsDictionary()
    let min_price = params['min_price']
    let max_price = params['max_price']
    if (min_price == 'NaN' || min_price == null){
        min_price = global_min_price
        max_price = global_max_price
    }
    $("#slider").slider("values", [min_price, max_price])
    
    minamount = $('#minamount')[0]
    maxamount = $('#maxamount')[0]

    minamount.value = min_price + ' ₽'
    maxamount.value = max_price + ' ₽'

    slider.slider({change: () => {sendAjax()}});

}

function updateSortBy(){
    let params = cookiesParamsDictionary()

    let current_sort_by_param = params['ordering']

    if (current_sort_by_param == 'Алфавит'){
        current_sort_by_param = 'Алфавиту'
    } else if (current_sort_by_param == 'Цена to-high'){
        current_sort_by_param = 'Цена (по возрастанию)'
    } else if (current_sort_by_param == 'Цена to-low'){
        current_sort_by_param = 'Цена (по убыванию)'
    } else if (current_sort_by_param == 'Скидка'){
        current_sort_by_param = 'Скидке'
    } else{
        current_sort_by_param = 'Алфавит'
    }

    $('.nice-select span.current')[0].innerText = current_sort_by_param
}

function setForCategory(item){
    let link = $(item).attr('href')
    setCookie('params', `?category=${link}&ordering=Алфавит`, 1)
    setCookie('page', 1, 1)
}

$('.sidebar__item ul li').on('click', function(){
    setForCategory(this);
});

