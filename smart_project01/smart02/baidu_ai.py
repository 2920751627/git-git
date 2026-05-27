import os
from aip import AipFace
import base64

from pypinyin import lazy_pinyin, Style


class BaiDuFace:
    # 注册应用有的
    def __init__(self, APP_ID=None, API_KEY=None, SECRET_KEY=None):
        if APP_ID is None:
            APP_ID = os.environ.get('BAIDU_FACE_APP_ID', '7756322')
        if API_KEY is None:
            API_KEY = os.environ.get('BAIDU_FACE_API_KEY', '06MCDmCFrWWQn558AXkoOl5Z')
        if SECRET_KEY is None:
            SECRET_KEY = os.environ.get('BAIDU_FACE_SECRET_KEY', 'YMIECcdCgcZdWPr0baeb8BnzIeJhBzOS')
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipFace(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    # 注册人脸
    def add_user(self, file_obj, userId):
        # 把图片转成base64
        image = base64.b64encode(file_obj.read()).decode('utf-8')
        imageType = "BASE64"
        groupId = "100"
        # userId = "dilireba" # 用人名拼音
        """ 调用人脸注册 """
        # client.addUser(image, imageType, groupId, userId);

        """ 如果有可选参数 """
        options = {}
        options["user_info"] = "这是迪丽热巴"
        options["quality_control"] = "NORMAL"
        options["liveness_control"] = "LOW"
        options["action_type"] = "REPLACE"
        """ 带参数调用人脸注册 """
        res = self.client.addUser(image, imageType, groupId, userId)

        return res

    # 删除人脸
    def delete(self, userId, faceToken):
        groupId = "100"
        """ 调用人脸删除 """
        res = self.client.faceDelete(userId, groupId, faceToken)
        return res

    # 搜索人脸
    def search(self, file_obj):
        image = base64.b64encode(file_obj.read()).decode('utf-8')
        imageType = "BASE64"
        groupIdList = "100"
        """ 调用人脸搜索 """
        res = self.client.search(image, imageType, groupIdList);
        return res

    # 人名转拼音
    def name_to_pinyin(self, text):
        style = Style.TONE3
        name_list = lazy_pinyin(text, style=style)
        return ''.join(name_list)