// background.js

document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('background-toggle');

    // 从 localStorage 加载背景颜色
    const savedColor = localStorage.getItem('backgroundColor');
    if (savedColor) {
        document.body.style.backgroundColor = savedColor;
        updateColorsBasedOnBackground(savedColor);
    }

    toggleButton.addEventListener('click', function() {
        // 获取当前背景颜色
        const currentColor = document.body.style.backgroundColor;

        // 切换背景颜色和文字颜色
        let newColor;
        if (currentColor === 'black') {
            newColor = 'rgb(74, 68, 255)';
        } else if (currentColor === 'rgb(74, 68, 255)') {
            newColor = 'white';
        } else {
            newColor = 'black';
        }

        document.body.style.backgroundColor = newColor;
        updateColorsBasedOnBackground(newColor);

        // 将背景颜色存储到 localStorage
        localStorage.setItem('backgroundColor', newColor);
    });

    function updateColorsBasedOnBackground(backgroundColor) {
        // 根据背景颜色更新文字和链接颜色
        if (backgroundColor === 'black') {
            document.body.style.color = 'white';
            updateLinkColors('white', 'transparent');
            updateMenuBackground('transparent');
            updateButtonStyle('#6d44ff', 'white', '#4a44ff', 'white');
        } else if (backgroundColor === 'rgb(74, 68, 255)') {
            document.body.style.color = 'white';
            updateLinkColors('white', 'transparent');
            updateMenuBackground('transparent');
            updateButtonStyle('white', 'black', 'gray', 'black'); 
        } else {
            document.body.style.color = 'black';
            updateLinkColors('black', 'transparent');
            updateMenuBackground('transparent');
            updateButtonStyle('black', 'white', '#6d44ff', 'white'); 
        }
    }

    function updateLinkColors(color, background) {
        // 更新链接文字颜色
        document.querySelectorAll('.menu li a,.menu span a,.cc ul,.cc li,.cc li h2,.cc li p').forEach(link => {
            link.style.color = color;
            link.style.backgroundColor = background;
        });
    }

    function updateMenuBackground(background) {
        // 更新菜单背景颜色
        document.querySelector('.menu').style.backgroundColor = background;
        document.querySelectorAll('.comment-box').forEach(box => {
            box.style.backgroundColor = background;
            //box.style.color = color;
        });
    }

    function updateButtonStyle(backgroundColor, color, hoverBackgroundColor, hoverColor) {
        // 更新按钮背景颜色和文字颜色
        toggleButton.style.backgroundColor = backgroundColor;
        toggleButton.style.color = color;

        // 清除之前的事件监听器
        toggleButton.removeEventListener('mouseenter', mouseEnterHandler);
        toggleButton.removeEventListener('mouseleave', mouseLeaveHandler);

        // 悬停时更改颜色
        function mouseEnterHandler() {
            toggleButton.style.backgroundColor = hoverBackgroundColor;
            toggleButton.style.color = hoverColor;
        }

        // 鼠标离开时恢复颜色
        function mouseLeaveHandler() {
            toggleButton.style.backgroundColor = backgroundColor;
            toggleButton.style.color = color;
        }

        // 添加悬停事件监听器
        toggleButton.addEventListener('mouseenter', mouseEnterHandler);
        toggleButton.addEventListener('mouseleave', mouseLeaveHandler);
    }


    // 页面加载时，检查 localStorage 中是否有背景图片
    const storedImage = localStorage.getItem('backgroundImage');
    if (storedImage) {
        document.body.style.backgroundImage = `url(${storedImage})`;
        document.body.style.backgroundSize = 'cover';
        document.body.style.backgroundPosition = 'center';
    }

    // 页面加载时，检查 localStorage 中是否有字体大小
    const storedFontSize = localStorage.getItem('fontSize');
    if (storedFontSize) {
        updateFontSize(storedFontSize);
    }

    // 如果存在切换背景图片的按钮，则添加其功能
    const backgroundButton = document.getElementById('background-picture');
    if (backgroundButton) {
        backgroundButton.onclick = function() {
            const overlay = document.createElement('div');
            overlay.style.position = 'fixed';
            overlay.style.top = '0';
            overlay.style.left = '0';
            overlay.style.width = '100%';
            overlay.style.height = '100%';
            overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
            overlay.style.display = 'flex';
            overlay.style.justifyContent = 'center';
            overlay.style.alignItems = 'center';
            overlay.style.zIndex = '1000';

            const uploadDiv = document.createElement('div');
            uploadDiv.style.backgroundColor = '#fff';
            uploadDiv.style.padding = '20px';
            uploadDiv.style.borderRadius = '5px';
            uploadDiv.innerHTML = `
                <h3>上传背景图片</h3>
                <input type="file" id="imageUpload" accept="image/*">
                <button id="setBackground">设置背景</button>
                <button id="close">关闭</button>
            `;

            overlay.appendChild(uploadDiv);
            document.body.appendChild(overlay);

            document.getElementById('setBackground').onclick = function() {
                const file = document.getElementById('imageUpload').files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        const imageUrl = e.target.result;
                        // 设置背景图片
                        document.body.style.backgroundImage = `url(${imageUrl})`;
                        document.body.style.backgroundSize = 'cover';
                        document.body.style.backgroundPosition = 'center';
                        // 将背景图片保存在 localStorage
                        localStorage.setItem('backgroundImage', imageUrl);
                    };
                    reader.readAsDataURL(file);
                }
                document.body.removeChild(overlay);
            };

            document.getElementById('close').onclick = function() {
                document.body.removeChild(overlay);
            };
        };
    }

    // 字体大小控制
    const fontSizeSlider = document.getElementById('font-size-slider');
    const increaseFontButton = document.getElementById('increase-font');

    if (fontSizeSlider && increaseFontButton) {
        // 页面加载时，设置滑块的位置为当前字体大小
        if (storedFontSize) {
            fontSizeSlider.value = storedFontSize;
        }

        // 监听滑块的变化以调整字体大小
        fontSizeSlider.addEventListener('input', function() {
            const newFontSize = fontSizeSlider.value;
            updateFontSize(newFontSize);
            // 将新字体大小保存在 localStorage
            localStorage.setItem('fontSize', newFontSize);
        });

        // 点击按钮增加字体大小
        increaseFontButton.addEventListener('click', function() {
            let currentFontSize = parseInt(window.getComputedStyle(document.body).fontSize);
            if (currentFontSize < 30) { // 最大字体大小为30px
                currentFontSize += 2;
                updateFontSize(currentFontSize);
                fontSizeSlider.value = currentFontSize; // 同步滑块的值
                // 将新字体大小保存在 localStorage
                localStorage.setItem('fontSize', currentFontSize);
            }
        });
    }

    // 更新页面所有元素的字体大小
    function updateFontSize(fontSize) {
        // 设置 body 的字体大小
        document.body.style.fontSize = fontSize + 'px';
        
        // 查找所有的 a 标签和其他特定元素，并更新它们的字体大小
        const allElements = document.querySelectorAll('body, body *');
        allElements.forEach(element => {
            element.style.fontSize = fontSize + 'px';
        });
    }

    const clearBackgroundButton = document.getElementById('clear-background');
    if (clearBackgroundButton) {
        clearBackgroundButton.onclick = function() {
            // 移除背景图片
            document.body.style.backgroundImage = 'none';
            // 从 localStorage 中移除背景图片条目
            localStorage.removeItem('backgroundImage');
        };
    }
});
document.getElementById('background-picture').onclick = function() {
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    overlay.style.display = 'flex';
    overlay.style.justifyContent = 'center';
    overlay.style.alignItems = 'center';
    overlay.style.zIndex = '1000';

    const uploadDiv = document.createElement('div');
    uploadDiv.style.backgroundColor = '#fff';
    uploadDiv.style.padding = '20px';
    uploadDiv.style.borderRadius = '5px';
    uploadDiv.innerHTML = `
        <h3>上传背景图片</h3>
        <input type="file" id="imageUpload" accept="image/*">
        <button id="setBackground">设置背景</button>
        <button id="close">关闭</button>
    `;
    
    overlay.appendChild(uploadDiv);
    document.body.appendChild(overlay);

    document.getElementById('setBackground').onclick = function() {
        const file = document.getElementById('imageUpload').files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imageUrl = e.target.result;
                // 设置背景图片
                document.body.style.backgroundImage = `url(${imageUrl})`;
                document.body.style.backgroundSize = 'cover';
                document.body.style.backgroundPosition = 'center';
                // 将背景图片保存在 localStorage
                localStorage.setItem('backgroundImage', imageUrl);
            };
            reader.readAsDataURL(file);
        }
        document.body.removeChild(overlay);
    };

    document.getElementById('close').onclick = function() {
        document.body.removeChild(overlay);
    };
};

// 页面加载时，检查 localStorage 中是否有背景图片
window.onload = function() {
    const storedImage = localStorage.getItem('backgroundImage');
    if (storedImage) {
        document.body.style.backgroundImage = `url(${storedImage})`;
        document.body.style.backgroundSize = 'cover';
        document.body.style.backgroundPosition = 'center';
    }
};
