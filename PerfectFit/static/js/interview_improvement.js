const improvementClickHandler = (event) => {
    const firstImprovement = document.querySelector('.interview-item');
    const contentEle = document.querySelector('.improvement-content');
    const answerEle = document.querySelector('.improvement-answer');
    const improvementsBtn = document.querySelectorAll('.btn');

    firstImprovement.classList.add('active');
    contentEle.innerHTML = improvements[0].improvement;
    answerEle.innerHTML = improvements[0].translatedAnswer;

    improvementsBtn.forEach(btn => {
        btn.addEventListener('click', (event) => {
            document.querySelectorAll('.interview-item')
                .forEach(btn => {
                    btn.classList.remove('active');
                });

            let currentTargetEle = event.target;

            while (!currentTargetEle.classList.contains('interview-item')) {
                currentTargetEle = currentTargetEle.parentElement;
            }

            currentTargetEle.classList.add('active');

            const id = event.target.dataset.improvementId;
            const filteredImprovement = improvements.filter(improvement => improvement.improvementId == id);

            if (filteredImprovement.length === 0) {
                alert('해당 개선 사항이 존재하지 않습니다.');
                return;
            }

            contentEle.innerHTML = filteredImprovement[0].improvement;
            answerEle.innerHTML = filteredImprovement[0].translatedAnswer;
        });
    });
};

const titleClickHandler = () => {
    const titleEle = document.querySelector('.title');
    const titleBtnEle = document.querySelector('#edit-title');
    const titleInputEle = document.querySelector('#change-input');
    const titleSaveBtnEle = document.querySelector('#change-btn');

    if (!titleEle || !titleBtnEle || !titleInputEle || !titleSaveBtnEle) {
        return;
    }

    const showHandler = () => {
        titleInputEle.value = titleEle.innerHTML;

        titleEle.classList.add('none');
        titleBtnEle.classList.add('none');
        titleInputEle.classList.remove('none');
        titleSaveBtnEle.classList.remove('none');
    };
    const saveHandler = async () => {
        const changedTitle = titleInputEle.value;
        if (changedTitle.trim() === '') {
            alert('제목을 입력해주세요.');
            return;
        }

        const initialCss = () => {
            titleEle.classList.remove('none');
            titleBtnEle.classList.remove('none');
            titleInputEle.classList.add('none');
            titleSaveBtnEle.classList.add('none');
        };

        // 제목 변경 API 호출
        try {
            const response = await instance.patch(`/interview/${interviewId}/title`, JSON.stringify({
                title: changedTitle
            }));

            if (response.status !== 204) {
                alert('제목 변경에 실패했습니다.');
                initialCss();
                return;
            }
        } catch (error) {
            alert('제목 변경에 실패했습니다.');
            initialCss();
            return;
        }

        titleEle.innerHTML = changedTitle;
        initialCss();
    };

    titleBtnEle.addEventListener('click', showHandler);
    titleInputEle.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            saveHandler();
        }
    });
    titleSaveBtnEle.addEventListener('click', saveHandler);
};

const fetchAddLike = async () => {
    const response = await instance.post(`/interview/${interviewId}/like`);

    if (response.status !== 204) {
        alert('좋아요 추가에 실패했습니다.');
    }
};

const fetchRemoveLike = async () => {
    const response = await instance.delete(`/interview/${interviewId}/like`);

    if (response.status !== 204) {
        alert('좋아요 삭제에 실패했습니다.');
    }
};

const likeHandler = () => {
    const likeBtnEle = document.querySelector('#like-btn');
    const likeIconELe = document.querySelector('#like-icon');
    const likeCountEle = document.querySelector('#like-count');

    if (!likeBtnEle) {
        return;
    }

    const clickHandler = async () => {
        try {
            if (!isLike) {
                likeBtnEle.classList.add('active');
                await fetchAddLike();
                likeCountEle.innerHTML = parseInt(likeCountEle.innerHTML) + 1;
                likeIconELe.setAttribute('src', '/static/img/like_active.svg');
            } else {
                likeBtnEle.classList.remove('active');
                await fetchRemoveLike();
                likeCountEle.innerHTML = parseInt(likeCountEle.innerHTML) - 1;
                likeIconELe.setAttribute('src', '/static/img/like.svg');
            }

            isLike = !isLike;
        } catch (error) {
            console.error(error);
            alert('좋아요 처리에 실패했습니다.');
        }
    };

    likeBtnEle.addEventListener('click', clickHandler);
};

const deleteHandler = async () => {
    const deleteBtnEle = document.querySelector('#delete-btn');
    if (!deleteBtnEle) {
        return;
    }

    const fetchDelete = async () => {
        const response = await instance.delete(`/interview/${interviewId}`);

        if (response.status !== 204) {
            alert('삭제에 실패했습니다.');
            return;
        }

        location.replace('/interview/list');
    };

    deleteBtnEle.addEventListener('click', async () => {
        if (confirm('정말 삭제하시겠습니까?')) {
            await fetchDelete();
        }
    });
};

window.addEventListener('load', () => {
    improvementClickHandler();
    titleClickHandler();
    likeHandler();
    deleteHandler();
});