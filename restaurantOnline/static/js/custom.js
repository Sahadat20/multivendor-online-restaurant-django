
$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url =  $(this).attr('data-url');
        
        $.ajax({ 
            type: 'GET',
            url: url,
           
            success : function(response){
                if(response.status=='login_required'){
                    Swal.fire({
                        title: response.message,
                        
                        icon: "info"
                      }).then(function(){
                        window.location = '/login'
                      });
                }
                else if(response.status=='Failed'){
                    Swal.fire({
                        title: response.message,
                        icon: "error"
                      })
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)

                    // subtotal, tax & grand total 
                    applyCartAmount(response.cart_amount['subtotal'],response.cart_amount['tax'],response.cart_amount['grand_total'])

                }
                
            }
        })
    })
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url =  $(this).attr('data-url');
        cart_id =  $(this).attr('cart-id');
        
        $.ajax({ 
            type: 'GET',
            url: url,
           
            success : function(response){
               
                if(response.status=='login_required'){
                    Swal.fire({
                        title: response.message,
                        
                        icon: "info"
                      }).then(function(){
                        window.location = '/login'
                      });
                }
                else if(response.status=='Failed'){
                    Swal.fire({
                        title: response.message,
                        icon: "error"
                      })
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)
                    // subtotal, tax & grand total 
                    applyCartAmount(response.cart_amount['subtotal'],response.cart_amount['tax'],response.cart_amount['grand_total'])
                    if(window.location.pathname=='/cart/'){
                    removeCartItem(response.qty, cart_id)
                      if(response.cart_counter['cart_count']<=0){
                        document.getElementById("empty-cart").style.display = "block";
                      }
                    }
                     

                }
                
                
            }
        })
    })
    $('.delete_cart').on('click', function(e){
        e.preventDefault();
        cart_id = $(this).attr('data-id');
        url =  $(this).attr('data-url');
        
        $.ajax({ 
            type: 'GET',
            url: url,
           
            success : function(response){
               
                
                if(response.status=='Failed'){
                    Swal.fire({
                        title: response.message,
                        icon: "error"
                      })
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    Swal.fire({
                        title: response.message,
                        icon: "success"
                      })
                      // subtotal, tax & grand total 
                     applyCartAmount(response.cart_amount['subtotal'],response.cart_amount['tax'],response.cart_amount['grand_total'])
                      removeCartItem(0, cart_id)
                      if(response.cart_counter['cart_count']<=0){
                        document.getElementById("empty-cart").style.display = "block";
                      }
                      
                }
                
                
            }
        })
    })

    // delte cart element if the qty is 0
    function removeCartItem(cartItemQty, cartId){
        if(cartItemQty <=0){
            // remove the cart element
            document.getElementById("cart-item-"+cartId).remove()
        }
    }

    function applyCartAmount(subtotal, tax, grand_total){
        if(window.location.pathname=='/cart/'){
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(grand_total)
        }
    }

    $('.item_qty').each(function(){
        var tbl_id = $(this).attr('id');
        var qty = $(this).attr('data-qty')
        console.log(qty)
        $('#'+tbl_id).html(qty)
    })
})