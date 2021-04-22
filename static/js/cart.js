// console.log("Rajapandi");

var updateBtn = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId', productId, "action", action);

        console.log("User", user);
        if(user === 'AnonymousUser'){
            addCookie(productId, action)   
        }
        else{
            UpdateUserOrder(productId, action)
        }
            
    })
}

function addCookie(productId, action) {
    console.log("Not Logged in");
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity': 1}
        }else{
            cart[productId]['quantity'] += 1
        }

    }
    if(action == 'remove'){
        cart[productId]['quantity'] -= 1
        if( cart[productId]['quantity'] <= 0) {
            console.log("Remove Item");
            delete cart[productId]
        }
    } 
    console.log('Cart', cart);
    document.cookie = 'cart=' +JSON.stringify(cart)+";domain=;path=/"
    location.reload()
}

function UpdateUserOrder(productId, action){
    console.log("User is logged in");
    var url = '/update-item/'
    // console.log("URL", url);
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken

        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) => {
        console.log("data", data);
        location.reload()
    })
}