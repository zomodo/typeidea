import uuid

USER_KEY = 'uid'
TEN_YEARS = 60*60*24*365*10 # 十年

# 把自定义的middleware配置到setting中MIDDLEWARE下
class UserIDMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):
        uid=self.generate_uid(request)
        request.uid=uid         # 给request添加uid属性，在后面views可以拿到并使用
        response=self.get_response(request)
        response.set_cookie(USER_KEY,uid,max_age=TEN_YEARS,httponly=True)   # 设置cookie，httponly只在服务端能访问
        return response

    def generate_uid(self,request):
        try:
            uid=request.COOKIES[USER_KEY]
        except KeyError:
            uid=uuid.uuid4().hex
        return uid
