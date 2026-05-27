import api from '../../config/settings'
Page({

  data: {
    banner_list: [{
      img: ''
    }],
    notice: '社区最大交友平台上线社区最大交友平台上线啦社区最大交友平台上线啦'
  },

  // 向后端发送请求-->声明周期--》页面加载好了--》向后端发送请求
  onLoad() {
    wx.request({
      url: api.banner,
      method:'GET',
      success:(res)=>{
        this.setData({
          banner_list:res.data.banner,
          notice:res.data.notice.title
        })
      }
    })
  },



  gotoCollection() {
    wx.navigateTo({
      url: '/pages/collection/collection',
    })
  },
  gotoActivity() {
    wx.switchTab({
      url: '/pages/activity/activity',
    })
  },
  gotoFace() {
    wx.navigateTo({
      url: '/pages/face/face',
    })
  },
  gotoVoice() {
    wx.navigateTo({
      url: '/pages/voice/voice',
    })
  },
  gotoHeart() {
    wx.navigateTo({
      url: '/pages/ai_speak/ai_speak',
    })
  },
  gotoGoods() {
    wx.navigateTo({
      url: '/pages/goods/goods',
    })
  },

})