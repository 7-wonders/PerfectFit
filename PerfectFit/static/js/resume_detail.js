// 좋아요
async function actionLike() {
    const likeButton = document.getElementById("like-button");
    const likeCountSpan = document.getElementById("like-count");

    // isLike 상태를 토글
    isLike = !isLike;

    // UI 상태 업데이트(API 연결 시 삭제 후 if 204 안에 있는 코드로 대체)
    if (isLike) {
        likeButton.classList.add("liked");
        likeCount += 1; // 좋아요 증가
    } else {
        likeButton.classList.remove("liked");
        likeCount -= 1; // 좋아요 감소
    }

    // 좋아요 수 업데이트
    likeCountSpan.textContent = likeCount;
    try {
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
    } catch (error) {
        alert('좋아요 실패! 다시 시도해 주세요.');
    }
}

// 페이지네이션 관련 자기소개서 목록 업데이트
async function updateResumeList(pageNum) {
    // 페이지 번호를 갱신할 때마다 currentPage 값을 변경
    currentPage = pageNum;

    // startPage와 endPage 계산
    const newStartPage = Math.floor((pageNum - 1) / pageRange) * pageRange + 1;
    const newEndPage = Math.min(newStartPage + pageRange - 1, totalPages);

    // 새로 계산된 startPage, endPage를 업데이트
    updatePagination(newStartPage, newEndPage, totalPages);

    // 이력서 목록 업데이트 코드
    const resumeListContainer = document.getElementById("resume-list-container");

    if (!resumeListContainer) {
        console.log("container없음");
        return;
    }

    try {
        // 백엔드 호출
        const response = await axios.get(`/resume/test/list/${pageNum}`);
        const { resumes } = response.data;

        // 자기소개서 목록 초기화
        resumeListContainer.innerHTML = '';

        // 자기소개서 목록 생성
        resumes.forEach((resume) => {
            const resumeDiv = document.createElement("div");
            resumeDiv.classList.add("resume-list");

            resumeDiv.innerHTML = `
                <div>
                    <div class="resume-title">
                        <span class="title-category">${resume.occupationName} |</span>
                        <span class="title-category">${resume.jobName} |</span>
                        <span class="title-category">${resume.level}</span>
                        <a href="/resume/detail/${resume.resumeId}" class="resume-link">
                            <span class="Medium-20">${resume.title}</span>
                        </a>
                    </div>
                    <div style="margin-top: 10px;">
                        <img src="${resume.user.profilePath}" class="user-profile" />
                        <span class="Regular-16" style="margin-left: 5px">${resume.user.username}</span>
                        <span class="Regular-16-light" style="margin-left: 5px">
                            작성일: ${new Date(resume.createdTime).toLocaleDateString()}
                        </span>
                    </div>
                </div>
                <div class="resume-list-Engagement">
                    <div style="margin-right: 10px;">
                        <span uk-icon="icon: eye; ratio: 1.0;"></span>
                        <span class="Regular-16-light">${resume.viewCount}</span>
                    </div>
                    <div>
                        <button id="like-button" uk-icon="icon: heart; ratio: 1.0;" class="none-style-btn" onclick="actionLike()"></button>
                        <span id="like-count" class="Regular-16-light">${resume.likeCount}</span>
                    </div>
                </div>
            `;
            resumeListContainer.appendChild(resumeDiv);
            resumeListContainer.appendChild(document.createElement("hr"));
            console.log(`${pageNum}번 호출`);
        });

    } catch (error) {
        console.error("Error loading resume list:", error);
    }
}

// 페이지네이션 관련 코드
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

// 자기소개서 상세보기 삭제
async function removeResumeDetail(resumeId) {
    try {
        const response = await axios.delete(`/resume/${resumeId}`);

        if (response.status === 204) {
            alert('이력서가 삭제되었습니다.');
            window.location.href = "http://127.0.0.1:5000/user/mypage/resume"
        }
    } catch (error) {
        console.error('이력서 삭제 오류:', error);
        alert('삭제 실패! 다시 시도해 주세요.');
    }
}