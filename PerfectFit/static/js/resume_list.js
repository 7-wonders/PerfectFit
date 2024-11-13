document.addEventListener("DOMContentLoaded", function () {
    let activeIndex = -1;  // 현재 활성화된 탭을 추적하기 위한 변수

    // 처음에는 모든 콘텐츠를 숨기기
    document.querySelectorAll(".search-content, .search-content-level").forEach(content => content.style.display = "none");

    // 각 탭에 클릭 이벤트 추가
    document.querySelectorAll(".search-filter-wrapper li").forEach((tab, index) => {
        tab.addEventListener("click", function (event) {
            event.preventDefault();

            // 클릭된 탭에 따른 콘텐츠 요소 찾기
            const content = document.querySelectorAll(".search-content, .search-content-level")[index];

            // 동일한 탭을 다시 누른 경우, 콘텐츠를 숨기고 activeIndex를 초기화
            if (activeIndex === index) {
                content.style.display = "none";
                activeIndex = -1;
            } else {
                // 모든 콘텐츠 숨기기
                document.querySelectorAll(".search-content, .search-content-level").forEach(content => content.style.display = "none");

                // 클릭된 탭의 콘텐츠만 표시하고 activeIndex 업데이트
                content.style.display = "block";
                activeIndex = index;
            }
        });
    });
});
