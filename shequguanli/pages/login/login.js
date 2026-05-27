import api from '../../config/settings'
var app = getApp() // 取到 app.js 对象
Page({


  data: {
    name:'',
    phone: '',
    code: '',
    agreed: false,
    sendCodeDisabled: false,
    buttonText: '发送验证码',
    loading: false,
    timer: null,
    countDown: 60
  },

  // 监听手机号输入
  onPhoneInput(event) {
    this.setData({
      phone: event.detail
    });
  },

  // 监听验证码输入
  onCodeInput(event) {
    this.setData({
      code: event.detail
    });
  },

  // 发送验证码
  sendCode() {
    const phone = this.data.phone;
    wx.request({
      url: api.api_sendcode,
      method: 'POST',
      data: { phone: phone },
      success(res) {
        if (res.statusCode === 200) {
          wx.showToast({ title: '验证码已发送' });
        } else {
          wx.showToast({ title: res.data.error || '发送失败' });
        }
      }
    })
  },

  // 验证码倒计时
  countDown() {
    let countDown = this.data.countDown;
    if (countDown === 0) {
      clearInterval(this.data.timer);
      this.setData({
        buttonText: '发送验证码',
        sendCodeDisabled: false,
        countDown: 60
      });
      return;
    }
    this.setData({
      buttonText: countDown + 's',
      countDown: countDown - 1
    });
  },

  // 页面移走，销毁定时器
  onUnload() {
    clearInterval(this.data.timer);
  },

  //登录接口
  login() {
    const { phone, code } = this.data;
    wx.request({
      url: api.api_verifycode,
      method: 'POST',
      data: { phone, code },
      success(res) {
        if (res.statusCode === 200) {
          // 存储 token
          console.log(res.data)
          wx.setStorageSync('access_token', res.data.access);
          wx.setStorageSync('refresh_token', res.data.refresh);
          wx.showToast({ title: '登录成功' });
          app.globalData.userInfo = true;
          var name = res.data.name;
          var phone = res.data.phone;
         
          app.initUserInfo(name, 50,0,phone);
         
          // 跳转到首页
          wx.switchTab({
            url: '/pages/my/my',
          })
            
          
        } else {
          wx.showToast({ title: res.data.error || '验证失败' });
        }
      }
    })
  }
})