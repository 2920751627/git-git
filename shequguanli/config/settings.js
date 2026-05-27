const env = require('./env')

const rootUrl = env.API_BASE_URL

module.exports = {
  welcome: rootUrl + '/welcome/',
  banner: rootUrl + '/banner/',
  collection: rootUrl + '/collection/',
  area: rootUrl + '/area/',
  statistics: rootUrl + '/statistics/',
  face: rootUrl + '/face/',
  ai_speak: rootUrl + '/ai_speak/dynamic/',
  voice: rootUrl + '/voice/',
  notice: rootUrl + '/notice/',
  activity: rootUrl + '/activity/',
  api_sendcode: rootUrl + '/api/send-code/',
  api_verifycode: rootUrl + '/api/verify-code/',
  join: rootUrl + '/join/',
}
