document.getElementById('searchBox').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        search();
    }
});

const suggestionsDiv = document.getElementById('suggestions');
const searchBox = document.getElementById('searchBox');
const history = JSON.parse(localStorage.getItem('searchHistory')) || [];

searchBox.addEventListener('focus', () => showSuggestions(searchBox.value));

document.addEventListener('click', function(event) {
    if (!searchBox.contains(event.target) && !suggestionsDiv.contains(event.target)) {
        suggestionsDiv.style.display = 'none';
    }
});

function showSuggestions(value) {
    suggestionsDiv.innerHTML = '';
    if (!value) {
        suggestionsDiv.style.display = 'none';
        return;
    }

    const matchedSuggestions = history.filter(item => item.toLowerCase().includes(value.toLowerCase()));

    matchedSuggestions.forEach(item => {
        const suggestionItem = document.createElement('div');
        suggestionItem.className = 'suggestion-item';
        suggestionItem.textContent = item;
        suggestionItem.addEventListener('click', () => {
            searchBox.value = item;
            search();
        });
        suggestionsDiv.appendChild(suggestionItem);
    });

    suggestionsDiv.style.display = matchedSuggestions.length ? 'block' : 'none';
}

function search() {
    const query = searchBox.value;
    if (!query) return;

    if (!history.includes(query)) {
        history.push(query);
        localStorage.setItem('searchHistory', JSON.stringify(history));
    }

    let url;
    switch (query) {
        case '3C数码':
            url = '3C数码.html';
            break;
        case '服装百货':
            url = '服装百货.html';
            break;
        case '生活超市':
            url = '生活超市.html';
            break;
        case '小米14pro':
            url = '小米14pro.html';
            break;
        case 'RNW面膜':
            url = 'RNW面膜.html';
            break;
        case '伊利低脂高钙奶':
            url = '伊利低脂高钙奶.html';
            break;
        // 可以继续添加其他条件
        default:
            alert('未找到相关页面');
            return;
    }

    window.location.href = url;
}
