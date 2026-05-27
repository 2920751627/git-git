import api from '../../config/settings'

Page({

  data: {
    dataDict: {
      result: [{
          "id": 1,
          "name": "张铁蛋",
          "area": "#19",
          "avatar": "/images/img/b.jpg"
        },
        {
          "id": 2,
          "name": "刘亦菲",
          "area": "#19",
          "avatar": "/images/img/b.jpg"
        }
      ],
      today_count: 66,
    }
  },
  bindToForm()
  {
    wx.navigateTo({
      url: '/pages/form/form',
    })
  },

  refresh() {
    // 加载
    wx.showLoading({
      mask: true
    })
    wx.request({
      url: api.collection,
      method: 'GET',
      success: (res) => {
        console.log(res.data)
        if (res.data.code == 100) {
          this.setData({
            dataDict: res.data
          })
        } else {
          wx.showToast({
            title: '网络加载失败',
          })
        }
      },
      complete: () => {
        wx.hideLoading()
      },
    })
  },
  //页面加载好-发送请求---》发送请求方法别的地方也会有
  onLoad() {
    this.refresh()
  },
  // 下载重新加载
  onPullDownRefresh() {
    this.refresh();
  },

  // 删除这条记录
  doDeleteRow(e){
    wx.showModal({
      title: '确认是否删除?',
      complete: (res) => {
        if (res.cancel) {
          return
          
        }
        if (res.confirm) {
          // 真删除
          var nid =e.currentTarget.dataset.nid
          wx.showLoading({
            title: '删除中',
            mask:true
          })

          wx.request({
            url: api.collection+nid+'/',
            method:'DELETE',
            success:(res)=>{
              // 删除完成或没完成，都刷新页面
              this.refresh()

            },
            complete:()=>{
              wx.hideLoading()
            }
          })
          
        }
      }
    })

  },
  onShow(){
    this.refresh()
  },
  bindToStatistics(){
    wx.navigateTo({
      url: '/pages/statistics/statistics',
    })
  }
})