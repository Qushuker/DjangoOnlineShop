document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.toggle-favorites').forEach(function(button) {

        function updateFavoriteButton(button, isFavorite) {
            const img = button.querySelector('.heart');



            img.src = isFavorite ? heartIconPathOn : heartIconPathOff;

            button.setAttribute('data-favorited', isFavorite);
        }


        // Проверка при загрузке
        const productId = button.getAttribute('data-product-id');

        fetch(`/is_favorite/${productId}/`)
            .then(response => response.json())
            .then(data => {
                updateFavoriteButton(button, data.is_favorite);
            })
            .catch(error => console.error('Ошибка при проверке избранного:', error));

        button.addEventListener('click', function(event) {
            event.preventDefault();
            const isFavorited = this.getAttribute('data-favorited') === 'true';

            const url = isFavorited ? `/remove_from_favorites/${productId}/` : `/add_to_favorites/${productId}/`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify({ product_id: productId })
            })
                .then(response => {
                    if (response.ok) {
                        // Переключаем состояние кнопки
                        updateFavoriteButton(this, !isFavorited);
                    }
                })
                .catch(error => console.error('Ошибка:', error));
        });
    });
});