window.addEventListener('load', () => {
    const searchEle = document.getElementById('search');
    const iconEle = document.getElementById('icon');

    const search = (event) => {
        if (event && iconEle.contains(event.target)) {
            event.preventDefault();
        }

        const searchValue = searchEle.value;
        if (searchValue) {
            location.replace(`/interview/list/search?keyword=${searchValue}`);
        } else {
            alert('검색어를 입력해주세요.');
            searchEle.focus();
        }
    }

    iconEle.addEventListener('click', search);
    searchEle.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            search();
        }
    });
});