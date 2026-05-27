const rootUrl = 'http://10.239.219.201:8000/smart02'

// 表示导出---》在任意js中，可以导入--》导入就是这个对象
module.exports = {
  welcome: rootUrl + '/welcome/',
  banner: rootUrl + '/banner/',
  collection:rootUrl + '/collection/',
  area: rootUrl + '/area/',
  statistics: rootUrl + '/statistics/',
  face: rootUrl + '/face/',
  ai_speak: rootUrl + '/ai_speak/dynamic/',
  voice: rootUrl + '/voice/',
  notice:rootUrl + '/notice/',
  activity: rootUrl + '/activity/',
  api_sendcode: rootUrl + '/api/send-code/',
  api_verifycode: rootUrl + '/api/verify-code/',
  join:rootUrl+'/join/',

}
