const urlList = [
    '/interview/list',
    '/interview/list/job',
    '/interview/list/search'
];

window.addEventListener('load', () => {
   const url = window.location.pathname;
    const navList = document.querySelectorAll('.nav-item');

    navList.forEach((nav, index) => {
        if (url === urlList[index]) {
            nav.classList.add('active');
        } else {
            nav.classList.remove('active');
        }
    });
});