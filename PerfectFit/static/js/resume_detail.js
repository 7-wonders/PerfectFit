function actionLike() {
    const likeButton = document.getElementById("like-button");
    const likeCountSpan = document.getElementById("like-count");

    // isLike 상태를 토글
    isLike = !isLike;

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

    // // API 요청을 위한 데이터 준비
    // const requestData = {
    //     headers: {
    //         "Content-Type": "application/json",
    //         "Authorization": "Bearer your-auth-token" // 실제 Authorization 토큰으로 대체
    //     },
    //     body: JSON.stringify({
    //         isLike: isLike
    //     }),
    //     method: "POST"
    // };
    //
    // // API 호출
    // fetch("/like-api-endpoint", requestData)
    //     .then(response => {
    //         if (!response.ok) {
    //             throw new Error("API 요청 실패");
    //         }
    //         return response.json();
    //     })
    //     .then(data => {
    //         console.log("API 요청 성공:", data);
    //     })
    //     .catch(error => {
    //         console.error("API 요청 중 오류 발생:", error);
    //
    //         // 오류가 발생하면 상태 롤백
    //         isLike = !isLike;
    //         if (isLike) {
    //             likeButton.classList.add("liked");
    //         } else {
    //             likeButton.classList.remove("liked");
    //         }
    //     });
}

