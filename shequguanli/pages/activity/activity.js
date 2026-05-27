import api from '../../config/settings'
var app = getApp() // 取到 app.js 对象
Page({
  data: {
    activityList: [

    ]
  },
  onLoad(){
    this.refresh()
  },
  refresh(){
    wx.showLoading({
      mask:true,
    })
    wx.request({
      url: api.activity,
      method:'GET',
      success:(res)=>{
        this.setData({
          activityList:res.data
        })
      },
      complete:()=>{
        wx.hideLoading()
      }
    })
  },

  // 活动报名接口
  handleSignup: function (event) {
    var app = getApp();
    var info = app.globalData.userInfo;
    if (!info) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
  
    var activityId = event.mark.id;   // 活动 id
    var username = info;     // 从全局数据取手机号（即 username）
    console.log(username)
    wx.request({
      
      url: api.join + '?activity_id=' + activityId,   // 活动 id 通过查询参数传递
      method: 'POST',
      data: { username: username },                   // 只发 username
      header: {
        'Authorization': 'Bearer ' + info.token       // JWT 认证
      },
      success: (res) => {
        wx.showToast({ title: res.data.msg || '报名成功', icon: 'success' });
      },
      fail: () => {
        wx.showToast({ title: '网络错误', icon: 'none' });
      }
    });
  }
})
