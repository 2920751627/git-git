import api from '../../config/settings'
Page({

  data: {
    avatar: '/images/camera/camera.png',
    objectArray: [{
        id: 1,
        name: '2单元1号楼',
        desc: '2#1'
      },
      {
        id: 2,
        name: '2单元2号楼',
        desc: '2#2'
      }
    ],
    name: '',
    index: -1
  },

  bindToCamera() {
    wx.navigateTo({
      url: '/pages/camera/camera',
    })
  },
  onLoad() {
    wx.request({
      url: api.area,
      method: "GET",
      success: (res) => {
        this.setData({
            objectArray: res.data
          }

        )
      }
    })
  },

  //选中某个网格回显
  bindPickerChange(e) {
    this.setData({
      index: e.detail.value
    })

  },

  // 上传图片
  postUser(e) {
    wx.showLoading({
      title: '提交中',
      mask: true
    })
    // 上传文件
    wx.uploadFile({
      url: api.collection,
      filePath: this.data.avatar,
      name: 'avatar',
      formData: {
        name: this.data.name,
        area: this.data.objectArray[this.data.index].id // 选中了那个区域的id
      },
      success: (res) => {
        // 跳转回上一页
        wx.navigateBack({})
      },
      complete: () => {
        wx.hideLoading()
      }

    })

  }
})


