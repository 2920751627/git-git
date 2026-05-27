// pages/welcome/welcome.js
import api from '../../config/settings'
Page({
  data: {
    second:3,
    img:''
  },
  doJump(){
    // 点击就跳转到首页
    wx.switchTab({
      url: '/pages/index/index',
    })
  },


  onLoad(options) {
   wx.request({
      url: api.welcome,
      method:'GET',
      success:(res)=>{
       
        if(res.data.code==100){
          this.setData({
            img:res.data.result          
          })
          
        }else{
          wx.showToast({
            title: '网络请求异常',
          })
        }
      }
    })



    // 启动定时器，倒计时
    // 清除定时器
    var instance=setInterval(()=>{
      if(this.data.second<=0){
        // 把定时器清除
        clearInterval(instance)
        //跳转到index页面
        wx.switchTab({
          url: '/pages/index/index',
        })
      }else{
        this.setData({
          second:this.data.second-1
        })
      }

 
    },1000)

  },

})