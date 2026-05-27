import api from '../../config/settings'
var app = getApp() // 取到 app.js 对象
Page({


  data: {
    userInfo: null,
  },
  // 手机号快速登录
  getPhoneNumber(event) {
    console.log(event)
    // 通过获取手机号返回的code--传递给后端--后端调用：POST https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token=ACCESS_TOKEN -->获取手机号--》后端签发token给前端
    wx.request({
      url: api.quick_login,
      method: 'POST',
      data: {
        code: event.detail.code
      },
      success: (res) => {
        console.log(res)
        //在此返回登录信息，用户登录
        var data = res.data;
        console.log(data)
        if (data.code == 100) {
          console.log('---', data)
          var token = data.token
          var name = data.name
          var score = data.score
          var avatar = data.avatar
          app.initUserInfo(name, score, avatar, token)
          var info = app.globalData.userInfo
          console.log('globalData.userInfo', info)
          if (info) {
            this.setData({
              userInfo: info
            })
          }
        } else {
          wx.showToast({
            title: '登录失败',
          })
        }
      }

    })

  },
  handleOtherLogin() {
    wx.navigateTo({
      url: '/pages/login/login',
    })
  },

  onShow() {
    // 1 取出放在app.js 中的用户信息，赋值到当前的userInfo中，userInfo只要有值--》页面就显示用户信息了
    var info = app.globalData.userInfo
    console.log('globalData.userInfo', info)
    if (info) {
      this.setData({
        userInfo: info
      })
    }
  },
  handleLogout() {
    // 1 调用app.js 的退出
    app.logoutUserInfo()
    // 2 当前页面中到的userInfo值为空
    this.setData({
      userInfo: null
    })
  }
})