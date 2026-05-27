from django.core.cache import cache
from django.conf import settings

def store_sms_code(phone, code):
    """将验证码存入缓存，key 为 sms_code_{phone}，过期时间 5 分钟"""
    cache.set(f"sms_code_{phone}", code, timeout=settings.SMS_CODE_EXPIRE_SECONDS)

def verify_sms_code(phone, code):
    """校验验证码，成功返回 True 并删除缓存（一次性有效）"""
    stored_code = cache.get(f"sms_code_{phone}")
    if stored_code and stored_code == code:
        cache.delete(f"sms_code_{phone}")  # 验证后立即删除，防止重复使用
        return True
    return False