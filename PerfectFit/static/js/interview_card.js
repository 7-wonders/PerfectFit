window.addEventListener('load', () => {
    console.log('Interview card js loaded');
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('click', () => {
            let interviewId = card.dataset.interviewId;
            if (!interviewId) {
                alert('페이지 이동 중 오류가 발생하였습니다.');
                return;
            }
            interviewId = parseInt(interviewId, 10); // 또는 Number(interviewId)
            console.log("Redirecting to interview improvement page with ID:", interviewId);

            window.location.href = `/interview/improvement/${interviewId}`;
        });
    });
});