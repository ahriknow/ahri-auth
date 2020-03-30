import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
	state: {
		refresh: '',
		token: localStorage.getItem('token')
	},
	mutations: {
		refresh(state, time) {
			state.refresh = time
		},
		token(state, token) {
			localStorage.setItem('token', token)
			state.token = token
		}
	},
	actions: {},
	modules: {}
})
