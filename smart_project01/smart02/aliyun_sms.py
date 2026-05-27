import random
from alibabacloud_dysmsapi20170525.client import Client as DysmsapiClient
from alibabacloud_dysmsapi20170525 import models as dysmsapi_models
from alibabacloud_tea_openapi import models as open_api_models
from django.conf import settings

def create_sms_client():
    """创建阿里云短信客户端"""
    config = open_api_models.Config(
        access_key_id=settings.ALIBABA_CLOUD_ACCESS_KEY_ID,
        access_key_secret=settings.ALIBABA_CLOUD_ACCESS_KEY_SECRET,
    )
    config.endpoint = settings.ALIBABA_SMS_ENDPOINT
    return DysmsapiClient(config)

def send_sms_code(phone_number: str, code: str) -> bool:
    """开发模式：控制台打印验证码，不真实发送"""
    print("\n" + "=" * 40)
    print(f"【模拟短信】手机号：{phone_number}")
    print(f"【模拟短信】验证码：{code}")
    print("=" * 40 + "\n")
    return True
    """发送短信验证码，成功返回 True"""
    #client = create_sms_client()
    #request = dysmsapi_models.SendSmsRequest(
       # phone_numbers=phone_number,
       # sign_name=settings.ALIBABA_SMS_SIGN_NAME,
        #template_code=settings.ALIBABA_SMS_TEMPLATE_CODE,
        #template_param=f'{{"code":"{code}"}}',   # 模板变量，与模板中 ${code} 对应
    #)
    #try:
      #  response = client.send_sms(request)
      #  if response.body.code == 'OK':
      #      return True
      #  else:
      #      print(f"短信发送失败: {response.body.message}")
       #     return False
   # except Exception as e:
       # print(f"短信发送异常: {e}")
       # return False#

def generate_code(length=6):
    """生成纯数字验证码"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])