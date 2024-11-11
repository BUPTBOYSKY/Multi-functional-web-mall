document.addEventListener('DOMContentLoaded', function () {
    const reduceButtons = document.querySelectorAll(".reduceCss");
    const addButtons = document.querySelectorAll(".addCss");
    const deleteButtons = document.querySelectorAll(".deleteItem");

    // 获取 CSRF Token
    function getCSRFToken() {
        const tokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        if (tokenElement) {
            return tokenElement.value;
        } else {
            console.error("CSRF token not found.");
            return null;
        }
    }

    // 更新购物车请求
    function updateCartItem(itemId, action) {
        const csrfToken = getCSRFToken();
        if (!csrfToken) return;

        fetch('/mixiaozi/update_cart_item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ 'item_id': itemId, 'action': action })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();  // 更新页面以反映最新的购物车状态
            } else {
                alert(data.error || "更新购物车失败，请重试！");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // 删除购物车请求
    function deleteCartItem(itemId) {
        const csrfToken = getCSRFToken();
        if (!csrfToken) return;

        fetch('/mixiaozi/delete_cart_item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ 'item_id': itemId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();  // 更新页面以反映删除后的购物车状态
            } else {
                alert(data.error || "删除商品失败，请重试！");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // 绑定加号按钮事件
    addButtons.forEach(button => {
        button.addEventListener('click', function () {
            const itemId = button.dataset.itemId;
            updateCartItem(itemId, 'add');
        });
    });

    // 绑定减号按钮事件
    reduceButtons.forEach(button => {
        button.addEventListener('click', function () {
            const itemId = button.dataset.itemId;
            updateCartItem(itemId, 'reduce');
        });
    });

    // 绑定删除按钮事件
    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();  // 阻止链接的默认行为
            const itemId = button.dataset.itemId;
            deleteCartItem(itemId);
        });
    });
});
