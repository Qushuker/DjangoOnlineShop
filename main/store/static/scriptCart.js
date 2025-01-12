$(document).ready(function() {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function updateButtonText(button, quantity) {
        if (quantity > 0) {
            // Если в корзине уже есть товар
            button.text(quantity);
        } else {
            // Если товар отсутствует
            button.text('Add');
        }
    }


    // Количество товара в корзине
    // При загрузке главной страницы
    $('.add-to-cart-button').each(function() {
        var productId = $(this).data('product-id');
        var button = $(this);

        $.ajax({
            type: 'GET',
            url: '/get_cart_item_quantity/' + productId + '/',
            success: function(response) {
                // Обновляем текст на кнопке
                updateButtonText(button, response.quantity);
            },
            error: function(response) {
                console.error('Ошибка при получении количества');
            }
        });
    });

    // Обработчик клика для добавления товара в корзину
    $('.add-to-cart-button').click(function(e) {
        e.preventDefault();
        var productId = $(this).data('product-id');
        var button = $(this);

        $.ajax({
            type: 'POST',
            url: '/add_to_cart/' + productId + '/',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            },
            success: function(response) {
                // Обновляем количество товара на кнопке
                updateButtonText(button, response.quantity);
                updateCartTotalItems()
            },
            error: function(response) {
                console.error('Ошибка при добавлении');
            }
        });
    });
    // Плюс в корзину
    $('.increase').click(function(e) {
        e.preventDefault();
        const productId = $(this).data('id');
        $.ajax({
            url: `/increase_quantity/${productId}/`,
            method: 'POST',
            success: function(response) {
                $('#cart').html(response);
                updateCartTotalItems()
            }
        });
    });

    // Минус из корзины
    $('.decrease').click(function(e) {
    e.preventDefault();
    const productId = $(this).data('id');
    $.ajax({
    url: `/decrease_quantity/${productId}/`,
    method: 'POST',
    success: function(response) {
    $('#cart').html(response);
    updateCartTotalItems()
}
});
});

    // Удалить товар из корзины
    $('.remove').click(function(e) {
    e.preventDefault();
    const productId = $(this).data('id');
    $.ajax({
    url: `/remove_from_cart/${productId}/`,
    method: 'POST',
    success: function(response) {
    $('#cart').html(response);
    updateCartTotalItems()
}
});
});
    function updateCartTotalItems() {
        fetch('/api/cart/total-items/')
            .then(response => response.json())
            .then(data => {
                // Обновляем значение на странице
                document.getElementById('cart-total-items').textContent = data.total_items;
            })
            .catch(error => console.error('Error:', error));
    }


});
