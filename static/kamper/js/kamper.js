/**
 * Created by Paige on 7/25/16.
 * core KAMPER:
 * 1. submitLanguage()
 * 2. submitOrder(product_number)
 * 3. submitAddCart(product_number)
 * 4. function post(path, params, method)
 */



function chat() {
    // var Tawk_API = Tawk_API || {}, Tawk_LoadStart = new Date();
    // (function () {
    //     var s1 = document.createElement("script"), s0 = document.getElementsByTagName("script")[0];
    //     s1.async = true;
    //     s1.src = 'https://embed.tawk.to/57c90ae5a767d83b45f1bda4/default';
    //     s1.charset = 'UTF-8';
    //     s1.setAttribute('crossorigin', '*');
    //     s0.parentNode.insertBefore(s1, s0);
    // })();
    //

    window.$zopim||(function(d,s){var z=$zopim=function(c){z._.push(c)},$=z.s=
        d.createElement(s),e=d.getElementsByTagName(s)[0];z.set=function(o){z.set.
    _.push(o)};z._=[];z.set._=[];$.async=!0;$.setAttribute("charset","utf-8");
        $.src="//v2.zopim.com/?4BXojPCuUfaKXTUzjm4HyKPOFjTXDaay";z.t=+new Date;$.
            type="text/javascript";e.parentNode.insertBefore($,e)})(document,"script");

}





function deletecart(){

    var chkbox = document.getElementsByName("chkboxpnum");
    var chkboxchecked = [];
    var cnt = 0;
    for(var i = 0 ; i < chkbox.length ; i++){

        if(chkbox[i].checked){
            chkboxchecked.push(chkbox[i].value);
            //alert(chkbox[i].value);
            cnt++;
        }
    }

    if(cnt == 0){

        alert("Please tick items you want to remove");
        return;

    }


    var rem = document.getElementById("remove_item");
    var hiddenCheckField = document.createElement("input");

    hiddenCheckField.setAttribute("type", "hidden");
    hiddenCheckField.setAttribute("name", "checked");
    hiddenCheckField.setAttribute("value", chkboxchecked);

    rem.appendChild(hiddenCheckField);
    rem.submit();


}



function allCheckBox() {


    var bool = document.getElementById("all_checked").checked;
    var pnumArr = document.getElementsByName("chkboxpnum");
    for(var i = 0 ; i < pnumArr.length ; i++){
        pnumArr[i].checked = bool;
    }
}

function submitLanguage(){
    /***
     * author: Genus
     * Function: submitLanguage()
     * funt: submit Language Form, if Language Form is changed.
     ***/

    var language_form = document.getElementById("language_selector");
    language_form.submit();
}

function submitOrder(product_number){

    //return post(base_url,)


}

function submitAddCart(product_number,csrf_token){

    var base_url= "/basket/add/";
    var path = base_url+product_number+'/';
    console.log(path);
    console.log(typeof(product_number));

    var quantity = document.getElementById("order-quantity").value;

    return post(path, {quantity: quantity});

}

function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}
