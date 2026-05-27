import api from '../../config/settings'
Page({

  /**
   * 页面的初始数据
   */
  data: {
    dataList:[]

  },
  onLoad(){
    this.getRecord()
  },

  getRecord(){
    wx.showLoading({mask:true})
    wx.request({
      url: api.statistics,
      method:"GET",
      success :(res) =>{
        this.setData({
          dataList:res.data
        })
      },
      complete:()=>{
        wx.hideLoading()
      }
    })
  }
})
