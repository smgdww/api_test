# 主要实现用户添加，修改，删除和查询

# 要继承Base，可以使用Base中的方法
from api.base import Base
from loguru import logger

class UserManager(Base):  # 创建一个用户管理的类，类里包括了用户增删改查等的方法


    # 初始化接口路径:
    def __init__(self):
        self.add_user_url = self.get_url("/admin/admin/create")
        self.edit_user_url = self.get_url("/admin/admin/update")
        self.search_user_url = self.get_url("/admin/admin/list?page=1&limit=20&sort=add_time&order=desc")
        self.delete_user_url = self.get_url("/admin/admin/delete")


    # 新增管理员
    def add_user(self,username,password,**kwargs):
        """
        请求的添加管理员的接口
        :return:添加管理员接口返回的json数据
        """
        user_data = {"username":username,"password":password} # 定义必填参数
        if kwargs:  # 判断是否有可选参数，如果有就更新到必填参数中
            logger.info("添加管理员可选参数:{}",**kwargs)
            user_data.update(**kwargs)
        return self.post(self.add_user_url,user_data)



    # 查询管理员
    def search_user(self):
        """
        请求查询管理员接口
        :return:查询管理员接口返回的数据
        """
        return self.get(self.search_user_url)




    # 修改管理员
    def edit_user(self,id,username,password,**kwargs):
        """
        请求修改管理员接口
        :return:修改管理员接口返回的数据
        """
        user_data = {"id":id,"username":username,"password":password}
        if kwargs:
            logger.info("查询管理员可选参数:{}", **kwargs)
            user_data.update(**kwargs)
        return self.post(self.edit_user_url,user_data)



    # 删除管理员
    def delete_user(self,id,username,**kwargs):
        """
        请求删除管理员接口
        :return:删除管理员接口返回的数据
        """
        user_data = {"id":id,"username":username}
        if kwargs:
            logger.info("删除管理员可选参数:{}",**kwargs)
            user_data.update(**kwargs)
        return self.post(self.delete_user_url, user_data)