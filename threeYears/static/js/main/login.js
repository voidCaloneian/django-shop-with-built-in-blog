//  DOM элементы
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

const loginButton = document.getElementById('login');
const loginPhoneNumberField = document.getElementsByName('phone_number')[1];
const loginFormLabel = $('label')[1];

const registerButton = document.getElementById('register');
const registerPhoneNumberField = document.getElementsByName('phone_number')[0];
const registerFormLabel = $('label')[0];

const registerErrorMessage = $('.text-danger.position-absolute')[0];
const loginErrorMessage = $('.text-danger.position-absolute')[1];

const registerCode = $('#registerCode')[0];
const loginCode = $('#loginCode')[0];

//  Остальные переменные
let loginPhoneNumber = null;
let registerPhoneNumber = null;
let loginFlag = false;
let registerFlag = false;

function checkFieldLength(login, phone){
    length = phone? 17 : 6
    if (login){
        if (loginPhoneNumberField.value.length == length){
            return true
        }
    } else{
        if (registerPhoneNumberField.value.length == length){
            return true
        }
    }
    return false
}

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

$(document).ready(function(){
    $('.phone').each(function(){
        $(this).mask('+0 (000) 000 0000');
    });
    $(".sms_code").click(function(clicked_object){
        if ($(clicked_object.target).hasClass("show")){
            let phone_number
            if ($(clicked_object.target).attr('id') == 'loginCode') {
                phone_number = loginPhoneNumber;
            } else {
                phone_number = registerPhoneNumber;
              }
            sendSmsCodeRequest(phone_number)
        }
    });
});

function check_phone_number(login = true){
    let phone_number
    if (login){
        phone_number = loginPhoneNumberField.value
        loginPhoneNumber = phone_number
    } else{
        phone_number = registerPhoneNumberField.value
        registerPhoneNumber = phone_number
    }

    return new Promise((resolve) => {
        $.ajax({
            type:'GET',
            url :'/user/check_phone_number/',
            data:{
                'phone_number':phone_number
            }, success: function(){
                resolve(true)
            }, error: function(){
                resolve(false)
            }
        })
    })
}

loginButton.addEventListener('click', (e) =>{
    e.preventDefault();
    if (loginFlag == false){
        if (checkFieldLength(true, true)){
            check_phone_number(login=true).then(exist => {
                if (exist == true) {
                    reformForSMS(login=true)
                } else{
                    showObject(loginErrorMessage)
                }
            })
        } else {showObject(registerErrorMessage)}
    } else{
        confirmCode(login=true).then(accessed =>{
            if (accessed==true){
                window.location.href = getCookie('last_page')
            } else{
                loginErrorMessage.innerText = 'Неверный код'
                showObject(loginErrorMessage)
            }
        })
    }
})

registerButton.addEventListener('click', (e) =>{
    e.preventDefault();
    if (registerFlag == false){
        if (checkFieldLength(false, true)){
            check_phone_number(login = false).then(exist => {
                if (exist != true) {
                    reformForSMS(login=false)
                } else{
                    showObject(registerErrorMessage)
                }
            })
        } else {showObject(registerErrorMessage)}
    } else{
        confirmCode(login=false).then(accessed =>{
            if (accessed==true){
                window.location.href = getCookie('last_page')
            } else{
                registerErrorMessage.innerText = 'Неверный код'
                showObject(registerErrorMessage)
            }
        })
    }
}) 

function hideObject(_object){
    _object.classList.remove('show')
    _object.classList.add('hide')
    
}

function showObject(_object){
    _object.classList.add('hide')
    _object.classList.remove('hide')
    _object.classList.add('show')
}

function reformForSMS(login = true) {
  const phoneNumberField = login ? loginPhoneNumberField : registerPhoneNumberField;
  const formLabel = login ? loginFormLabel : registerFormLabel;
  const phoneNumber = login ? loginPhoneNumber : registerPhoneNumber;
  const errorMessage = login ? loginErrorMessage : registerErrorMessage;
  const code = login ? loginCode : registerCode;

  login ? loginFlag = true : registerFlag = true;
  
  $(phoneNumberField).val('');
  formLabel.classList.add('code');
  formLabel.innerText = 'Введите код';
  sendSmsCodeRequest(phoneNumber);
  hideObject(errorMessage);
  showObject(code);
  unmaskAndRestrict(login);
}


function unmaskAndRestrict(login=true){
    if (login){
        field = $(loginPhoneNumberField)
    } else{
        field = $(registerPhoneNumberField)
    }
    field.unmask()
    field.attr({"maxlength": 6, "minlength": 6})
}


function sendSmsCodeRequest(phone_number){
    $.ajax({
        type:'GET',
        url :'/user/generate_sms_code',
        data:{
            'phone_number' : phone_number
        }
    })
}

function confirmCode(login=true){
    if (login){
        data = {
            'phone_number' : loginPhoneNumber,
            'sms_code': loginPhoneNumberField.value,
            'login': 'true'
        }
    } else{
        data = {
            'phone_number' : registerPhoneNumber,
            'sms_code': registerPhoneNumberField.value
        }
    }

    return new Promise((resolve) => {
        $.ajax({
            type:'GET',
            url :'/user/sms_code_verification/',
            data:data,
            success: function(){
                resolve(true)
            }, error: function(){
                resolve(false)
            }
        })
    })
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