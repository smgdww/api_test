

"""
作用:主要用于所有接口的公共功能，使用一个基类(父类)

功能1:处理url
功能2:重新封装get方法，post方法
功能3:处理头(headers)信息
功能4:登录(因为所有功能都基于登陆后)

"""

from setting import BASE_URL,LOGIN_INFO
import requests
from loguru import logger
from cacheout import Cache
"""
cacheout:主要用于缓存.
1.导入:from cacheout import Cache
2.设置缓存:cache.set(key,value) ==> cache.set("name","张三")
3.获取缓存:cache.get(key)   ==> cache,get("name")
"""
cache = Cache()  # 创建了cache对象

class Base():


    # 处理url，实现url的拼接
    def get_url(self,path,params=None):
        """
        返回一个完整的url
        :param path:接口路径:/admin/auth/login
        :param params:查询参数:/admin/admin/list?page=1&limit=20&sort=add_time&order=desc
        :return:full_url:http://121.196.13.152:8080/admin/auth/login
        """
        if params:  # 这代表params有参数的时候相当于Ture
            full_url = BASE_URL + path + params
            return full_url
        return BASE_URL + path

    # 重写get方法
    def get(self,url):
        result = None
        response = requests.get(url,headers=self.get_headers())
        try:
            result = response.json()  # 获取响应体中的json数据
            logger.success("请求URL:{},返回结果:{}".format(url,result))
            return result
        except  Exception as e:
            logger.error("请求get方法异常，返回数据为:{}".format(result))



    # 重写post方法
    def post(self,url,data):
        """
        在原来post的方法上新增日志以及直接返回json格式
        :return:
        """
        result = None
        response = requests.post(url,json=data,headers=self.get_headers())
        try:
            result = response.json()  # 获取响应体中的json数据
            logger.success("请求URL:{},请求参数:{},返回结果:{}".format(url,data,result))
            return result
        except  Exception as e:
            logger.error("请求post方法异常，返回数据为:{}".format(result))


    # 实现所有头信息的处理
    def get_headers(self):
        """
        处理请求头
        :return:返回的是字典格式的请求头,多是包括了Content-Type，X-Litemall-Admin-Token
        """
        headers = {"Content-Type":"application/json"}
        token = cache.get("token")  # 获取缓存中的值
        if token:
            headers.update({"X-Litemall-Admin-Token":token})
            return headers
        return headers


    # 实现登录功能
    def login(self):
        """
        通过调用登录接口获取token值，然后将其进行缓存。其他接口使用时，直接从缓存中取值。
        若没有取到，再调用登录接口，再将token值放在缓存中
        :return:
        """
        login_path = "/admin/auth/login"
        login_url = self.get_url(login_path)  # 拼接登录接口地址
        result = self.post(login_url,LOGIN_INFO)  # 请求登录接口，返回json数据
        try:
            if 0 == result.get("errno"):
                logger.info("请求登录接口成功")
                token = result.get("data").get("token")
                cache.set("token",token)
            else:
                logger.error("登陆失败:{}".format(result))
                return None
        except Exception as e:
            logger.error("请求登录接口失败，异常数据:{}".format(result))
            logger.error("报错信息:{}".format(e))



if __name__ == '__main__':
    base = Base()
    # print(base.get_url("/admin/admin/create"))
    # print(base.get_url("/admin/admin/list","?page=1&limit=20&sort=add_time&order=desc"))
    login_url = base.get_url("/admin/auth/login")
    login_data = {"username":"admin123","password":"admin123"}
    print(base.post(login_url,login_data))
