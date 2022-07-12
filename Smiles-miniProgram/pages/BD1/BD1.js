// pages/BD1/BD1.js
const app=getApp();
Page({

  /**
   * 页面的初始数据
   */
    data: {

    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        this.setData({
          uuid:options.uuid,
          cate:options.cate,
          pg:0
        });
        var self=this
        wx.request({
          url: app.globalData.url+'/predict/', // request for url/predict/
          method:"GET",
          header:{'Content-Type':'application/json'},
          data:{ 
              cate:options.cate,  // get the argument 
              uuid:options.uuid,
          },
          success:function(res){
            //console.log(res)
            self.setData({
              data:res.data // data has been saved
            })
          }
        })
    },
    chooseImage:function(){
      var self=this;
      wx.chooseImage({
        count: 1,
        sizeType:['original','compressed'],
        sourceType:['album','camera'],
        success:function(res){
          //console.log(res)
          wx.showLoading({
            title: '正在上传文件',
          });
          var img_src =res.tempFilePaths[0];
          const upload_task =wx.uploadFile({
            filePath: img_src,
            name: 'img',
            url: app.globalData.url+'/predict/',
            formData:{ cate:self.options.cate},
            success:function(res){
              console.log(res)
              wx.showToast({
               title: '上传识别成功',
               icon:"success",
               duration:1000
              })
              self.setData({img_src});
              //jump
              var data =JSON.parse(res.data); // Json?
              var url = "BD1?cate="+data.cate+"&uuid="+data.uuid; // the same dict
              setTimeout(function(){
                  wx.redirectTo({
                    url: url,
                  })
              });
            }
          });
          // progress symbol
          upload_task.onProgressUpdate((res)=>{
            self.setData({pg:res.progress});
          });
        },
      });
    }


})