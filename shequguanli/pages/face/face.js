import api from '../../config/settings'
Page({

  data: {
    backFront:true,
    record:[]
  },
  switchCamera(e) {
    var old = this.data.backFront
    this.setData({
      backFront: !old
    })
  },
  takePhoto(e){
    // 1 打开loading
    wx.showLoading({
      title: '检测中',
      mask:true
    })
    //2 拿到相机对象，拍照
    const ctx = wx.createCameraContext()
    ctx.takePhoto({
      quality: 'high',
      success: (res) => {
        //3 res中会有拍摄的照片
        console.log(11111),
        console.log('临时图片路径：', res.tempImagePath),
        // 4 把照片传到后端
        wx.uploadFile({
          url: api.face,
          filePath: res.tempImagePath,
        
          name: 'avatar',
          success:(response)=>{
            // 5 上传成功，后端返回数据
            
            let resdata = JSON.parse(response.data)
            if(resdata.code==100 || resdata.code==102){
              resdata.avatar = res.tempImagePath
              var oldRecord = this.data.record
              oldRecord.unshift(resdata)
              console.log(oldRecord)
              this.setData({
                record:oldRecord
              })

            }else{
              wx.showToast({
                title: '请正常拍照'
              })
            }
          },
          complete:function(){
            wx.hideLoading()
          }
        })
      }
    })
  },

})