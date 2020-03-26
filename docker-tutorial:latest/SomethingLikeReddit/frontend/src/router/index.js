import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

// import { authGuard } from "../auth/authGuard";

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/categories',
    name: 'categories',
    component: () => import('../views/Categories.vue')
  },
  {
    path: '/post',
    name: 'NewPost',
    component: () => import('../views/NewPost.vue')
  },
  {
    path: '/categories/:id',
    name: 'category',
    component: () => import('../views/Category.vue')
  },
  {
    path: '/profile/:id',
    name: 'profile',
    component: () => import('../views/Profile.vue')
  },
  {
    path: '/posts/:id',
    name: 'postSingle',
    component: () => import('../views/PostSingle.vue'),
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
