/*  ---------------------------------------------------
    Template Name: Ogani
    Description:  Ogani eCommerce  HTML Template
    Author: Colorlib
    Author URI: https://colorlib.com
    Version: 1.0
    Created: Colorlib
---------------------------------------------------------  */

'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");

        /*------------------
            Gallery filter
        --------------------*/
        $('.featured__controls li').on('click', function () {
            $('.featured__controls li').removeClass('active');
            $(this).addClass('active');
        });
        if ($('.featured__filter').length > 0) {
            var containerEl = document.querySelector('.featured__filter');
            var mixer = mixitup(containerEl);
        }
    });

    /*------------------
        Background Set
    --------------------*/

  
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css({'background-image' : 'url(' + bg + ')'});
    });

    //Humberger Menu
    $(".humberger__open").on('click', function () {
        $(".humberger__menu__wrapper").addClass("show__humberger__menu__wrapper");
        $(".humberger__menu__overlay").addClass("active");
        $("body").addClass("over_hid");
    });

    $(".humberger__menu__overlay").on('click', function () {
        $(".humberger__menu__wrapper").removeClass("show__humberger__menu__wrapper");
        $(".humberger__menu__overlay").removeClass("active");
        $("body").removeClass("over_hid");
    });

    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*-----------------------
        Categories Slider
    ------------------------*/
    $(".categories__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 4,
        dots: false,
        nav: true,
        navText: ["<span class='fa fa-angle-left'><span/>", "<span class='fa fa-angle-right'><span/>"],
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        responsive: {

            0: {
                items: 1,
            },

            480: {
                items: 2,
            },

            768: {
                items: 3,
            },

            992: {
                items: 4,
            }
        }
    });


    $('.hero__categories__all').on('click', function(){
        $('.hero__categories ul').slideToggle(400);
    });

    /*--------------------------
        Latest Product Slider
    ----------------------------*/
    $(".latest-product__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 1,
        dots: false,
        nav: true,
        navText: ["<span class='fa fa-angle-left'><span/>", "<span class='fa fa-angle-right'><span/>"],
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true
    });

    /*-----------------------------
        Product Discount Slider
    -------------------------------*/
    $(".product__discount__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 3,
        dots: true,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        responsive: {

            320: {
                items: 1,
            },

            480: {
                items: 2,
            },

            768: {
                items: 2,
            },

            992: {
                items: 3,
            }
        }
    });

    /*---------------------------------
        Product Details Pic Slider
    ----------------------------------*/
    $(".product__details__pic__slider").owlCarousel({
        loop: true,
        margin: 20,
        items: 4,
        dots: true,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true
    });

    /*-----------------------
		Price Range Slider
	------------------------ */
    var rangeSlider = $(".price-range"),
        minamount = $("#minamount"),
        maxamount = $("#maxamount"),
        minPrice = rangeSlider.data('min'),
        maxPrice = rangeSlider.data('max');
    rangeSlider.slider({
        range: true,
        min: minPrice,
        max: maxPrice,
        values: [minPrice, maxPrice],
        slide: function (event, ui) {
            minamount.val(ui.values[0] + ' ₽');
            maxamount.val(ui.values[1] + ' ₽');
        }
    });
    minamount.val(rangeSlider.slider("values", 0) + ' ₽');
    maxamount.val(rangeSlider.slider("values", 1) + ' ₽');

    /*--------------------------
        Select
    ----------------------------*/
    $("select").niceSelect();

    /*------------------
		Single Product
	--------------------*/
    $('.product__details__pic__slider img').on('click', function () {

        var imgurl = $(this).data('imgbigurl');
        var bigImg = $('.product__details__pic__item--large').attr('src');
        if (imgurl != bigImg) {
            $('.product__details__pic__item--large').attr({
                src: imgurl
            });
        }
    });

    /*-------------------
		Quantity change
	--------------------- */
    var proQty = $('.pro-qty');
    proQty.prepend('<span class="dec qtybtn">-</span>');
    proQty.append('<span class="inc qtybtn">+</span>');
    proQty.on('click', '.qtybtn', function () {
        var $button = $(this);
        var oldValue = $button.parent().find('input').val();
        if ($button.hasClass('inc')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            // Don't allow decrementing below zero
            if (oldValue > 1) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 1;
            }
        }
        changeProductAmount($button, newVal, true)
    });

})(jQuery);


function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
function eraseCookie(name) {   
    document.cookie = name+'=; Max-Age=-99999999;';  
}

function deleteIdFromList(id, cookies_list = null, page_is_shopping_cart = null){
    id = id.toString()
    // cookies_list == null тогда, когда функция вызвана кнопками удаления товара из корзины
    if ( cookies_list == null ){
        var cookies_list = getCookie('product_ids').split(' ')
    }
    // В новый массив добавляются лишь те элементы, которые не соответствуют удаляемому 'id'
    let filteredArray = cookies_list.filter(function(e) { return e.split('_')[0] !== id })
     setCookie('product_ids', filteredArray.join(' '))
    //  Если страница - страница корзины, то после удаления продукта из куки, он визуально удаляется на странице
    if (page_is_shopping_cart == true){
        removeProductInHtml(id, cookies_list.length)
        refreshTotalPrice()
        refreshCartWidgetCounter()
        refresh_shopping_cart_widget_balance()
    }

}


// Функция добавления товара в куки
function addOneProductIdToIds(id, amount = '1'){
    let cookies = getCookie('product_ids')

    // Если куки пустые, то устанавливаются новые
    if (!cookies){setCookie('product_ids', `${id}_${amount}`, 999999)}
    else{setCookie('product_ids', `${cookies} ${id}_${amount}`, 999999)}
}


// Функция добавляет продукт в куки, либо же удаляет его оттуда
function addOrDeleteProductId(id, amount = '1'){
    id = id.toString()
    let cookies = getCookie('product_ids')

    // Проверка на наличие продуктов в куках
    if (cookies){
        cookies = cookies.split(' ')
        // Создание листа, состоящего только из айди продуктов
        // Изначально лист состоит из элементов подобного стиля
        //               id_количествоТовара
        let cookies_list = []
        for (let i in cookies){
            let _id = cookies[i].split('_')[0]
            cookies_list.push(_id)
        }
        if (cookies_list.includes(id)){
            deleteIdFromList(id, cookies)
        } else {
            addOneProductIdToIds(id, amount)
        }

    // Если куков нет, то, очевидно, ожидается функция добавления продукта
    } else{ 
        addOneProductIdToIds(id, amount)
    }
    refresh_shopping_cart_widget_balance()
    refreshCartWidgetCounter()
}


// _____________________________________________________________________________

// Функция, которая преобразует куки продуктов в функционируемый словарь
function separator(){
    let products = getCookie('product_ids')
    if (products){
        products = products.split(' ')

        let dictionary = {}
    
    // Создаётся словарь, с подобным типом данных 
    //           {id:КоличествоТовара}
        for (let i in products){
            let item = products[i].split('_')
            dictionary[item[0]] = item[1]
        }
        return dictionary
    } else{ 
        return {}
    }
}

// Функция превращает функционированный словарь, созданный фунцией
//            'Separator', в обычный вид куков
function joinator(dictionary){
    let new_cookies = ''
    for (let item in dictionary){
        let amount = dictionary[item]
        new_cookies += `${item}_${amount} `
    }
    return new_cookies
}

// ---------------------------------------------------------------


// Функция, обновляющая значения количества
function setNewAmountValue(item, value, called_by_button = false){
    // Проверяет, вызвана ли функция кнопкой, либо же ручным вводом от пользователя
    if (called_by_button){
        // Визуальное обновление
        item = item.parent().find('input')
        $(item).val(value)
        var product_id = $(item).data('product_id')
    }else {
        var product_id = $(item).data('product_id') 
    }

    // Проверяет, добавлен ли продукт в корзину
    if (product_id){
        // Обновление количества в куках у соответствующего товара
        let products_dictionary = separator()
        products_dictionary[product_id] = parseInt(value)
        setCookie('product_ids', joinator(products_dictionary))
    }
}

// Функция, которая меняет количество продукта и обновляет финальную цену, вычисленную по формуле " цена_товара * количество_товара  "
function changeProductAmount(item, value, called_by_button=false){
    // Проверяет, вызвана функция кнопкой, либо же ручным вводом от пользователя
    if (called_by_button) {
        setNewAmountValue(item, value, called_by_button=true, )
        changeProductTotalPrice(item, value)
    }
    else{
        let value = item.value
        if (value < 1){value = 1; item.value = 1}
        setNewAmountValue($(item), value)
        changeProductTotalPrice($(item), value)
    }
    refreshTotalPrice()
    refreshCartWidgetCounter()
    refresh_shopping_cart_widget_balance()
}

var debounceTimer;

function saveScrollPosition() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(function() {
        var scrollPosition = window.pageYOffset || document.documentElement.scrollTop;
        setCookie('scroll_position', scrollPosition, 1);
  }, 250);
}

function nullScrollPosition(){
    setCookie('scroll_position', '', 1)
}

window.addEventListener('scroll', saveScrollPosition);

window.onload = () =>{
    scrollTo(0, getCookie('scroll_position'))
}

function saveLastPage() {
    var lastPage = getCurrentUrl()
    setCookie('last_page', lastPage, 1);
  }

function getCurrentUrl(){
    return window.location.href
}

function logout(){
    window.location.href = `/user/logout/?last_page=${getCurrentUrl()}`
}