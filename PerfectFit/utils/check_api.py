from flask import Request


def is_api_call(request: Request) -> bool:
    # 요청의 Content-Type 헤더가 JSON, Formdata인지 요구하는지 확인
    # 또한 Accept의 선호도에 따라 우선 순위를 둠
    # e.g Accept: application/json, text/html; q=0.9면 json은 1.0, formdata는 0.9로 나옴
    if request.content_type in ['application/json', 'multipart/form-data'] or \
            request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
        return True
    else:
        # HTML 페이지 응답 (일반 페이지 요청인 경우)
        return False
