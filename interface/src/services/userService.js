import api from './api'

export default {
  getCurrentUser() {
    return api.get('/user/me')
  }
}
