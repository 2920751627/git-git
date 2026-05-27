from django.urls import path
from .views import ActivityView,JoinActivityView
from rest_framework.routers import SimpleRouter
from .views import BannerView,CollectionView,AreaView,FaceView,StatisticsView,DynamicAISpeakView,FixedAISpeakView,VoiceView,NoticeView
from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import SendSmsCodeView, VerifyCodeView
router = SimpleRouter()
router.register('banner', BannerView, 'banner')
router.register('area', AreaView, 'area')
router.register('face', FaceView, 'face')
router.register('statistics', StatisticsView, 'statistics')
router.register('collection', CollectionView, 'collection')
router.register('voice', VoiceView, 'voice')
router.register('notice', NoticeView, 'notice')
router.register('activity', ActivityView, 'activity')



from .views import welcome
urlpatterns = [
    # http://127.0.0.1:8000/smart/welcome/-->>就能获得图片数据
    path('welcome/', welcome),
    path('ai_speak/fixed/', FixedAISpeakView.as_view(), name='fixed_ai_speak'),
    path('ai_speak/dynamic/',DynamicAISpeakView.as_view(), name='dynamic_ai_speak'),
    path('api/send-code/', SendSmsCodeView.as_view()),
    path('api/verify-code/', VerifyCodeView.as_view()),
    path('join/', JoinActivityView.as_view(), name='join'),
]
urlpatterns += router.urls

