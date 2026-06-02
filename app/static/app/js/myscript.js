$('#slider1, #slider2, #slider3 , #slider4 ,#slider5').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

function updateCartTotals(data) {
    document.getElementById('amount').innerText = data.amount
    document.getElementById('totalamount').innerText = data.totalamount

    var shippingRow = document.getElementById('shippingRow')
    var shippingAmount = document.getElementById('shippingAmount')
    if (shippingRow && shippingAmount) {
        if (data.ship) {
            shippingRow.firstChild.textContent = 'Shipping'
            shippingAmount.innerText = 'Rs. 70.00'
        } else {
            shippingRow.firstChild.textContent = 'Free delivery'
            shippingAmount.innerText = ''
        }
    }

    var cartItemCount = document.getElementById('cartItemCount')
    if (cartItemCount) {
        cartItemCount.innerText = data.cart_item_count
    }
}

function removeCartRow(productId, data) {
    var row = document.getElementById('cart-row-' + productId)
    if (row) {
        var separator = row.previousElementSibling
        if (separator && separator.tagName === 'HR') {
            separator.remove()
        }
        row.remove()
    }

    if (data.cart_empty) {
        var emptyCartMessage = document.getElementById('empty-cart-message')
        if (emptyCartMessage) {
            emptyCartMessage.style.display = 'block'
        }
        var cartColumn = document.querySelector('.col-sm-8')
        var totalsColumn = document.querySelector('.col-sm-4')
        if (cartColumn) {
            cartColumn.style.display = 'none'
        }
        if (totalsColumn) {
            totalsColumn.style.display = 'none'
        }
    }
}

$('.plus-cart').click(function(event){
    event.preventDefault();
    var id = $(this).attr('pid').toString();
    var eml = document.getElementById('quantity-' + id);
//    console.log(id)
    $.ajax({
    type:"GET",
    url:"/pluscart/",
    data : { prod_id:id } ,
    success:function(data){
        console.log(data)
//        console.log('data')
        eml.innerText = data.quantity
        updateCartTotals(data)
    }


    })
})


$('.minus-cart').click(function(event){
    event.preventDefault();
    var id = $(this).attr('pid').toString();
    var eml = document.getElementById('quantity-' + id);
//    console.log(id)
    $.ajax({
    type:"GET",
    url:"/minuscart/",
    data : {prod_id:id},
    success:function(data){
        console.log(data)
//        console.log('data')
        if (data.removed) {
            removeCartRow(id, data)
        } else {
            eml.innerText = data.quantity
        }
        updateCartTotals(data)
    }


    })
})


$('.remove-cart').click(function(event){
    event.preventDefault();
    var id = $(this).attr('pid').toString();
    console.log(id)
    $.ajax({
    type:"GET",
    url:"/removecart/",
    data : {prod_id:id},
    success:function(data){
        console.log(data)
        console.log('data')
        updateCartTotals(data)
        removeCartRow(id, data)
    }


    })
})
