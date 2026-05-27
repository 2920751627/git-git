from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Welcome,Banner,Notice,Collection,UserInfo,Area,Activity,JoinRecord

admin.site.register(Welcome)

admin.site.register(Banner)
admin.site.register(Notice)
admin.site.register(Collection)
admin.site.register(UserInfo)
admin.site.register(Area)
admin.site.register(Activity)
admin.site.register(JoinRecord)

