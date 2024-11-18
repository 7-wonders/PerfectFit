let isLiked = false; // 현재 유저가 좋아요를 눌렀는지 여부를 서버에서 받아와야 함
let likeCountValue = parseInt(document.getElementById('like-count').textContent, 10);

function actionLike() {
    const likeButton = document.getElementById('like-button');
    const likeCount = document.getElementById('like-count');

    // 좋아요 상태 변경
    isLiked = !isLiked; // 현재 상태 반대로 토글
    likeCountValue = isLiked ? likeCountValue + 1 : likeCountValue - 1;

    // UI 업데이트
    likeButton.classList.toggle('liked', isLiked); // liked 클래스 추가/제거
    likeButton.textContent = "안녕하세용?"
    likeCount.textContent = likeCountValue;

    // 서버에 상태 전송
    // fetch('/update-like-status', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({
    //         userId: 'currentUserId', // 실제 유저 ID로 교체해야 함
    //         resumeId: 'resumeId',   // 실제 이력서 ID로 교체해야 함
    //         isLiked: isLiked        // 현재 좋아요 상태 전달
    //     })
    // })
    // .then(response => {
    //     if (!response.ok) {
    //         throw new Error('좋아요 상태를 업데이트하는 데 실패했습니다.');
    //     }
    //     return response.json();
    // })
    // .catch(error => {
    //     console.error('에러 발생:', error);
    //
    //     // 에러 발생 시 UI를 롤백
    //     isLiked = !isLiked; // 상태 다시 원래대로
    //     likeCountValue = isLiked ? likeCountValue + 1 : likeCountValue - 1;
    //     likeButton.classList.toggle('liked', isLiked);
    //     likeCount.textContent = likeCountValue;
    // });
}