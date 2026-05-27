from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from datetime import datetime, date, timezone
from django.utils import timezone
from django.conf import settings

from .models import Welcome,Collection
def welcome(request):
    # 1 查出order最大的一张图片，返回给前端
    res = Welcome.objects.all().order_by('-order').first()
    img = settings.MEDIA_SERVER_URL + str(res.img)
    return JsonResponse({'code': 100, 'msg': '成功', 'result': img})

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin,DestroyModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin
from rest_framework.response import Response
from .models import Banner, Notice
from .serializer import BannerSerializer, NoticeSerializer,CollectionSerializer,CollectionSaveSerializer
class BannerView(GenericViewSet, ListModelMixin):
    queryset = Banner.objects.filter(is_delete=False).order_by('order')[:3]
    serializer_class = BannerSerializer


    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        # 获取最后一条通知
        notice = Notice.objects.all().order_by('-create_time').last()
        serializer = NoticeSerializer(instance=notice)

        return Response({'code': 100, 'msg': '成功', 'banner': res.data, 'notice': serializer.data})



from .models import Area,UserInfo
from .serializer import AreaSerializer
class AreaView(GenericViewSet,ListModelMixin):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class CollectionView(GenericViewSet, ListModelMixin, DestroyModelMixin, CreateModelMixin):
    queryset = Collection.objects.all().filter(
        create_time__gte=timezone.now().date()
    )

    def get_serializer_class(self):
        if self.action == 'create':
            return CollectionSaveSerializer
        return CollectionSerializer

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        today_count = len(self.get_queryset())
        return Response({
            'code': 100,
            'msg': '成功',
            'result': res.data,
            'today_count': today_count
        })

    def destroy(self, request, *args, **kwargs):
        from libs.baidu_ai import BaiDuFace
        instance = self.get_object()

        # 百度 AI 删除人脸
        baidu = BaiDuFace()
        res = baidu.delete(instance.name_pinyin, instance.face_token)
        print('百度删除结果:', res)

        # 本地删除
        self.perform_destroy(instance)
        return Response({'code': 100, 'msg': '删除成功'})


from django.db.models import Count
from django.db.models.functions import Trunc
from .models import Collection
from .serializer import StatisticsListSerializer
class StatisticsView(GenericViewSet, ListModelMixin):
    # 做个分组
    queryset = Collection.objects.annotate(date=Trunc('create_time', 'day')).values('date').annotate(
    count=Count('id')).values('date', 'count')
    serializer_class = StatisticsListSerializer


from .baidu_ai import BaiDuFace
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from .models import Collection


class FaceView(GenericViewSet):
    parser_classes = [MultiPartParser, JSONParser]  # ✅ 必须

    def create(self, request, *args, **kwargs):
        print("FILES:", request.FILES)  # ✅ 调试用

        avatar_object = request.FILES.get('avatar')  # ✅ 用 FILES
        if not avatar_object:
            return Response({'code': 103, 'msg': '请正常提交人脸'})

        ai = BaiDuFace()
        res = ai.search(avatar_object)

        if res.get('error_code') == 0:
            user_id = res['result']['user_list'][0]['user_id']
            score = int(res['result']['user_list'][0]['score'])
            user = Collection.objects.filter(name_pinyin=user_id).first()
            return Response({
                'code': 100,
                'msg': '匹配成功',
                'name': user.name,
                'score': score
            })
        else:
            return Response({'code': 102, 'msg': '非社区人员'})



from django.views.decorators.csrf import csrf_exempt


# views.py
import os
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from openai import OpenAI


class DynamicAISpeakView(APIView):
    """动态问题 AI 回答视图"""

    def get(self, request):
        # 获取前端传来的问题
        question = request.GET.get('question', '')

        if not question:
            return JsonResponse({
                'status': 'error',
                'message': '请提供问题参数'
            }, status=400)

        try:
            # 初始化 DeepSeek 客户端
            client = OpenAI(
                api_key=settings.DEEPSEEK_API_KEY,
                base_url=settings.DEEPSEEK_BASE_URL
            )

            # 调用 AI 回答问题
            messages = [{"role": "user", "content": question}]
            response = client.chat.completions.create(
                model=settings.DEEPSEEK_MODEL,
                messages=messages,
                stream=False,
                reasoning_effort="high",
                extra_body={"thinking": {"type": "enabled"}},
            )

            answer = response.choices[0].message.content

            return JsonResponse({
                'status': 'success',
                'data': {
                    'question': question,
                    'answer': answer
                }
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'AI 处理失败: {str(e)}'
            }, status=500)


class FixedAISpeakView(APIView):
    """固定问题 AI 回答视图（保留原来的）"""

    def get(self, request):
        try:
            client = OpenAI(
                api_key=settings.DEEPSEEK_API_KEY,
                base_url=settings.DEEPSEEK_BASE_URL
            )

            # 第一个问题
            messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]
            response = client.chat.completions.create(
                model=settings.DEEPSEEK_MODEL,
                messages=messages,
                stream=False,
                reasoning_effort="high",
                extra_body={"thinking": {"type": "enabled"}},
            )
            first_answer = response.choices[0].message.content

            # 第二个问题
            messages.append({"role": "assistant", "content": first_answer})
            messages.append({'role': 'user', 'content': "How many Rs are there in the word 'strawberry'?"})
            response = client.chat.completions.create(
                model=settings.DEEPSEEK_MODEL,
                messages=messages,
                stream=False,
                reasoning_effort="high",
                extra_body={"thinking": {"type": "enabled"}},
            )
            second_answer = response.choices[0].message.content

            return JsonResponse({
                'status': 'success',
                'data': {
                    'question1': {
                        'question': '9.11 and 9.8, which is greater?',
                        'answer': first_answer
                    },
                    'question2': {
                        'question': "How many Rs are there in the word 'strawberry'?",
                        'answer': second_answer
                    }
                }
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)


from libs.baidu_ai import BaiDuVoice


class VoiceView(GenericViewSet):
    def create(self, request, *args, **kwargs):
        voice_object = request.data.get('voice')
        # with open('./a.wav','wb') as f:
        #     f.write(voice_object.read())
        ai = BaiDuVoice()
        result = ai.speed(voice_object)
        # {'corpus_no': '6847771638436561158', 'result': ['你是不是打过来？'], 'sn': '15921476781594371078', 'err_msg': 'success.', 'err_no': 0}
        if result.get('err_no') == 0:
            return Response({'code': 100, 'msg': '识别成功', 'result': result.get('result')})
        else:
            return Response({'code': 101, 'msg': '识别失败'})


from .models import Notice
from .serializer import NoticeSerializer

class NoticeView(GenericViewSet, ListModelMixin):
    queryset = Notice.objects.all().order_by('create_time')
    serializer_class = NoticeSerializer


from .models import Activity
from .serializer import ActivitySerializer

class ActivityView(GenericViewSet, ListModelMixin):
    queryset = Activity.objects.all().order_by('date')
    serializer_class = ActivitySerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .aliyun_sms import send_sms_code, generate_code
from .cache import store_sms_code, verify_sms_code
from .serializer import SendCodeSerializer, VerifyCodeSerializer

User = get_user_model()

class SendSmsCodeView(APIView):
    """发送短信验证码"""
    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        # 1. 生成验证码
        code = generate_code()
        # 2. 存入缓存
        store_sms_code(phone, code)
        # 3. 发送短信
        success = send_sms_code(phone, code)
        if success:
            return Response({"message": "验证码已发送"}, status=status.HTTP_200_OK)
        else:
            # 发送失败，删除验证码缓存，返回错误
            from django.core.cache import cache
            cache.delete(f"sms_code_{phone}")
            return Response({"error": "短信发送失败，请稍后重试"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from faker import Faker



class VerifyCodeView(APIView):
    """验证码登录"""
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']

        # 验证码校验
        if not verify_sms_code(phone, code):
            return Response({"error": "验证码错误或已过期"}, status=status.HTTP_400_BAD_REQUEST)
        fake = Faker()
        random_username = fake.name()

        # 获取或创建用户（以手机号为 username）

        user, created = UserInfo.objects.get_or_create(
            mobile=phone,
            defaults={
                'name': random_username,

            }
        )
        # 生成 JWT token
        refresh = RefreshToken.for_user(user)
        return Response({
            "name":user.name,

            "message": "登录成功",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_id": user.id,
            "phone": user.mobile
        }, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import UserInfo, Activity, JoinRecord
from django.db.models import F

class JoinActivityView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1. 取前端传来的 username（手机号）做身份校验
        frontend_username = request.data.get('username')
        if not frontend_username:
            return Response({'msg': '缺少 username'}, status=400)


        # 2. 活动 id 从查询参数获取
        activity_id = request.query_params.get('activity_id')
        if not activity_id:
            return Response({'msg': '缺少 activity_id'}, status=400)
        activity = get_object_or_404(Activity, pk=activity_id)

        # 3. 通过手机号找到对应的 UserInfo（没有则创建）
        user_info, _ = UserInfo.objects.get_or_create(
            mobile=frontend_username,
            defaults={'name': frontend_username}
        )

        # 4. 利用 JoinRecord 检查是否已报名
        if JoinRecord.objects.filter(user=user_info, activity=activity).exists():
            return Response({'msg': '您已报名该活动'}, status=400)

        # 5. 创建报名记录
        JoinRecord.objects.create(user=user_info, activity=activity)
        updated = Activity.objects.filter(
            pk=activity.pk,
            count__lt=F('total_count')  # 报名人数未满
        ).update(count=F('count') + 1)
        return Response({'msg': '报名成功'})