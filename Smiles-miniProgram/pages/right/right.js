// pages/right/right.js
const app =getApp();
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

  },
  bindGetUserInfo:function(e){
   if (e.detail.userInfo){
        var that =this;
        that.setUserInforNext(e.detail.userInfo);
   }
   else{}
  },
  setUserInforNext:function(user_info){
    wx.showLoading({  // 等待图标
      title: '登录授权跳转',
    });
    wx.request({
      url: app.globalData.url+'/users/',
      data:{
        avatarUrl:user_info.avatarUrl,
        city:user_info.city,
        country:user_info.country,
        gender:user_info.gender,
        language:user_info.language,
        province:user_info.province
      },
      method:"POST",
      header:{'content-type':'application/json'},
      success:function(res){ console.log(res);},
    });
    setTimeout(()=>{
        wx.reLaunch({
          url: '../vision/vision',
        })
    },1000);
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})