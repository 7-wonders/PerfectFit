console.log(' !')

// 로그아웃
async function deleteCookie() {
     try {
         const response = await instance.post('/user/logout', JSON.stringify({
                refreshToken: refreshToken,
            }));
         if(response.status === 200) {
             location.reload();
         }
    } catch (error) {
        alert("로그아웃에 실패했습니다. 다시 시도해주세요.");
    }
}



document.addEventListener("DOMContentLoaded", async function() {
    if(login) {
         try {
            const response = await instance.get('/user/profile')
            profilePath = response.data;
            // console.log(profilePath);
            const userProfileImage = document.getElementById('userProfileImage');
            userProfileImage.src = profilePath;
        }
        catch(error) {
             alert("프로필 이미지 호출에 실패했습니다. 다시 시도해주세요.");
        }
    }
});