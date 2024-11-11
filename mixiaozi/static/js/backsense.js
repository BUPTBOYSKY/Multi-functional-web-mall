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