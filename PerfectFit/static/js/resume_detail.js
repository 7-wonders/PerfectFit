let startPage;
let endPage;
let currentPage = 1;
let pageRange = 5;
let totalPages;
let count = 5;
let total;
let response;
// 좋아요
async function actionLike(resumeId) {
    const likeButton = document.getElementById("like-button");
    const likeCountSpan = document.getElementById("like-count");
    // isLike 상태를 토글
    isLike = !isLike;
    try {
        if(isLike) {
            // post 요청을 백엔드로 보냄
            const response = await instance.post(`/resume/${resumeId}/like`, {
                body: {
                    isLike: isLike,
                }
            });
            if (response.status === 204) {
                // UI 상태 업데이트
                if (isLike) {
                    likeButton.classList.add("liked");
                    likeCount += 1; // 좋아요 증가
                } else {
                    likeButton.classList.remove("liked");
                    likeCount -= 1; // 좋아요 감소
                }
                // 좋아요 수 업데이트
                likeCountSpan.textContent = likeCount;
            }
        }
        else {
             // DELETE 요청을 백엔드로 보냄
            const response = await instance.delete(`/resume/${resumeId}/like`, {
                body: {
                    isLike: isLike,
                }
            });
            if (response.status === 204) {
                // UI 상태 업데이트
                if (isLike) {
                    likeButton.classList.add("liked");
                    likeCount += 1; // 좋아요 증가
                } else {
                    likeButton.classList.remove("liked");
                    likeCount -= 1; // 좋아요 감소
                }
            }
            // 좋아요 수 업데이트
            likeCountSpan.textContent = likeCount;
        }
    }
    catch (error) {
        alert('좋아요 실패! 다시 시도해 주세요.');
    }
}


// 페이지 로드 시 API 호출
document.addEventListener('DOMContentLoaded', async () => {
    try {
        response = await instance.get(`/resume?page=${currentPage}&count=${count}`);
    }
    catch(error) {
        console.log("자기소개서 목록 불러오기 실패");
    }
    renderResumeList(response.data.resumes);
    total = response.data.total;
    totalPages = Math.floor((total + pageRange - 1) / pageRange);
    startPage = Math.floor((currentPage - 1) / pageRange) * pageRange + 1;
    endPage = (startPage + pageRange - 1 <= totalPages) ? (startPage + pageRange - 1) : totalPages;
    updatePagination(startPage, endPage, totalPages);
});

// 페이지네이션 UI 만들기
function updatePagination(startPage, endPage, totalPages) {
    const paginationContainer = document.querySelector('.uk-pagination');

    paginationContainer.innerHTML = '';

    // 이전 버튼 추가
    if (startPage > 1) {
        const prevButton = document.createElement('li');
        prevButton.innerHTML = `
            <button class="pagination-btn Regular-20-light" onclick="updateResumeList(${startPage - 1})">
                <span class="Regular-20-light" uk-pagination-previous></span>
            </button>
        `;
        paginationContainer.appendChild(prevButton);
    }

    // 페이지 번호들 추가
    for (let pageNum = startPage; pageNum <= endPage; pageNum++) {
        const pageButton = document.createElement('li');
        pageButton.innerHTML = `
            <button class="pagination-btn Regular-20-light" onclick="updateResumeList(${pageNum})">
                <span id="page-${pageNum}" class="${pageNum === currentPage ? 'primary-20' : 'Regular-20-light'}">
                    ${pageNum}
                </span>
            </button>
        `;
        paginationContainer.appendChild(pageButton);
    }

    // 다음 버튼 추가
    if (endPage < totalPages) {
        const nextButton = document.createElement('li');
        nextButton.innerHTML = `
            <button class="pagination-btn Regular-20-light" onclick="updateResumeList(${endPage + 1})">
                <span class="Regular-20-light" uk-pagination-next></span>
            </button>
        `;
        paginationContainer.appendChild(nextButton);
    }
}

// 자기소개서 목록 및 페이지 번호 업데이트
async function updateResumeList(pageNum) {
    // 페이지 번호를 갱신할 때마다 currentPage 값을 변경
    currentPage = pageNum;

    // startPage와 endPage 계산
    const newStartPage = Math.floor((pageNum - 1) / pageRange) * pageRange + 1;
    const newEndPage = Math.min(newStartPage + pageRange - 1, totalPages);

    // 새로 계산된 startPage, endPage를 업데이트
    updatePagination(newStartPage, newEndPage, totalPages);
    try {
        response = await instance.get(`/resume?page=${pageNum}&count=${count}`);
    }
    catch(error) {
        console.log("자기소개서 목록 불러오기 실패");
    }
    renderResumeList(response.data.resumes);
    updatePagination(newStartPage, newEndPage, totalPages);
}

// 자기소개서 목록 렌더링
function renderResumeList(resumes) {
    const listContainer = document.getElementById('resume-list-container');
    listContainer.innerHTML = ''; // 초기화

    // resumes가 객체라면 for...in을 사용해 반복
    for (const num in resumes) {
            const resume = resumes[num];  // key를 사용하여 resume 데이터 접근
            const resumeHTML = `
                <div class="resume-list">
                    <!-- 게시물 왼쪽 -->
                    <div>
                        <div class="resume-title">
                            <span class="title-category">${resume.occupationName} |</span>
                            <span class="title-category">${resume.jobName} |</span>
                            <span class="title-category">${resume.level}</span>
                            <a href="/resume/${resume.resumeId}" class="resume-link">
                                <span class="Medium-20">${resume.title}</span>
                            </a>
                        </div>
                        <div style="margin-top: 10px;">
                            <img src="${resume.profilePath}" class="user-profile" />
                            <span class="Regular-16" style="margin-left: 5px;">${resume.username}</span>
                            <span class="Regular-16-light" style="margin-left: 5px;">
                                작성일: ${new Date(resume.createdTime).toLocaleDateString()}
                            </span>
                        </div>
                    </div>
                    <!-- 조회수 및 좋아요 -->
                    <div class="resume-list-Engagement">
                        <div style="margin-right: 10px;">
                            <span uk-icon="icon: eye; ratio: 1.0;"></span>
                            <span class="Regular-16-light">${resume.viewCount}</span>
                        </div>
                        <div>
                            <span id="like-button-${resume.resumeId}" uk-icon="icon: heart; ratio: 1.0;"
                                  class="${resume.isLike ? 'liked' : ''}"
                                  onclick="actionLike(${resume.resumeId})"></span>
                            <span id="like-count-${resume.resumeId}" class="Regular-16-light">${resume.likeCount}</span>
                        </div>
                    </div>
                </div>
                <hr>
            `;
            listContainer.innerHTML += resumeHTML;
    }
}

// 자기소개서 상세보기 삭제
async function removeResumeDetail(resumeId) {
    try {
        const response = await instance.delete(`/resume/${resumeId}`);

        if (response.status === 204) {
            alert('이력서가 삭제되었습니다.');
            window.location.href = "/user/mypage/resume"
        }
    } catch (error) {
        console.error('이력서 삭제 오류:', error);
        alert('삭제 실패! 다시 시도해 주세요.');
    }
}
