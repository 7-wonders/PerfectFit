from dataclasses import asdict

from flask import Blueprint, render_template, request

from dto.user.user import UserDto
from services.user_service import UserService

user_bp = Blueprint('user', __name__)


@user_bp.route('/users') ## 경로 확인필수
def get_users(): ## 인자없이 넘어온것이기에 바디로 넘어온 것 이라 칭함
    page = request.args.get('page', default=1, type=int) ## 바디로 넘어오면 어떤인자가 왔는지 모르기에 이 코드로 바디의 인자를 긁어옴
    count = request.args.get('count', default=10, type=int)
## 이제 이 줄에서 에러 핸들링 // 인자검사
    paginate_user = UserService.get_users(page, count) ## 서비스 호출
    response: UserDto.Response.Users = UserDto.Response.Users( ## 응답결과를 가공된 데이터를 사용할 것이다.
        users=[UserDto.Response.IntroUser(user.id, user.name) for user in paginate_user.items],
        pages=paginate_user.pages, ## 여기까지가 데이터 가공 (꾸미는) 작업
    )

    return render_template("users.html", users=asdict(response))


@user_bp.route('/user/<user_id>') # 변수 유저에 대한 디테일한 정보 얻어오기
def get_user(user_id: int): ## 이름맞춰주고 자료형 작성하면 인자가 받아와짐.
    user = UserService.get_user(user_id) ## 서비스로 호출
    if not user:
        return render_template("user.html")

    response: UserDto.Response.IntroUser = UserDto.Response.IntroUser(user.id, user.name)

    return render_template("user.html", user=response) ## 렌더 템플릿 페이지 띄워준다
