import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
	{
		path: '/auth',
		name: 'auth',
		component: () => import('../views/LoginAndSignup.vue')
	},
	{
		path: '/admin',
		alias: '/',
		name: 'admin',
		redirect: '/admin/userinfo',
		component: () => import('../views/Admin.vue'),
		children: [
			{
				path: 'userinfo',
				name: 'userinfo',
				component: () => import('../views/Admin/Userinfo.vue')
			},
			{
				path: 'department',
				name: 'department',
				component: () => import('../views/Admin/Department.vue')
			},
			{
				path: 'jurisdiction',
				name: 'jurisdiction',
				component: () => import('../views/Admin/Jurisdiction.vue')
			},
			{
				path: 'user',
				name: 'user',
				component: () => import('../views/Admin/User.vue')
			}
		]
	}
]

const router = new VueRouter({
	routes
})

export default router
