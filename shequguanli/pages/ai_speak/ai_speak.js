import api from '../../config/settings'
Page({
  data: {
    question: '',
    chatHistory: [],
    loading: false
  },

  onLoad: function() {
    // 从本地存储加载历史记录
    const history = wx.getStorageSync('ai_speak_history') || [];
    this.setData({ chatHistory: history });
  },

  // 输入框变化
  onQuestionChange: function(event) {
    this.setData({
      question: event.detail
    });
  },

  // 提问 AI
  askAI: function() {
    const question = this.data.question.trim();
    
    if (!question) {
      wx.showToast({
        title: '请输入问题',
        icon: 'none'
      });
      return;
    }

    this.setData({ loading: true });

    // 调用后端 API
    wx.request({
      url: api.ai_speak,  // 动态问题接口
      method: 'GET',
      data: {
        question: question
      },
      header: {
        'content-type': 'application/json'
      },
      success: (res) => {
        if (res.data.status === 'success') {
          const newChatItem = {
            question: question,
            answer: res.data.data.answer
          };
          
          // 更新聊天记录
          const updatedHistory = [newChatItem, ...this.data.chatHistory];
          
          this.setData({
            chatHistory: updatedHistory,
            question: '',  // 清空输入框
            loading: false
          });
          
          // 保存到本地存储
          wx.setStorageSync('ai_speak_history', updatedHistory.slice(0, 50)); // 最多保存50条
          
        } else {
          wx.showToast({
            title: res.data.message || '获取答案失败',
            icon: 'none'
          });
          this.setData({ loading: false });
        }
      },
      fail: (err) => {
        console.error('请求失败:', err);
        wx.showToast({
          title: '网络请求失败',
          icon: 'none'
        });
        this.setData({ loading: false });
      }
    });
  },

  // 清空历史记录
  clearHistory: function() {
    wx.showModal({
      title: '提示',
      content: '确定要清空所有聊天记录吗？',
      success: (res) => {
        if (res.confirm) {
          this.setData({ chatHistory: [] });
          wx.removeStorageSync('ai_spaek_history');
          wx.showToast({
            title: '已清空',
            icon: 'success'
          });
        }
      }
    });
  }
});