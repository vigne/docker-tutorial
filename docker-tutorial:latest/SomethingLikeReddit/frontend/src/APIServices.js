import axios from 'axios'
import {EJSON} from 'bson'
import router from './router'

// axios.defaults.baseURL = '/api' // to be used in productin mode

console.log(process.env.VUE_APP_BACKEND_BASEURI)
axios.defaults.baseURL = process.env.VUE_APP_BACKEND_BASEURI  // to be used in development mode
axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.token}`

const options = {
  transformResponse: [(data) => {
    // transform the response from MongoDB BSON-string proper JavaScript object
    return EJSON.parse(data);
  }]
}

export class APIService{

  constructor(){
  }
  init() {
      console.log("init db")
      const url = `/init_db`;
      return axios.post(url).then(response => response.data)
  }
  getFeaturedPosts() {
      console.log("get featured")
      const url = `/posts`;
      return axios.get(url, options).then(response => response.data)
  }
  getCategories() {
      console.log("get categories")
      const url = `/categories`
      return axios.get(url, options).then(response => response.data)
  }
  getPostByCategory(categoryId) {
    console.log("get post by category")
    const url = `/category/${categoryId}`;
    return axios.get(url, options)
      .then(response => response.data)
      .catch((error) => {
        if (error.response && error.response.status === 401)
          router.push('/login')
        console.log("Error requesting post from backend", error)
      })
  }

  getPostById(postId) {
    console.log("get post by id", postId)
    if(postId === undefined)
      return
    const url = `/posts/${postId}`;
    return axios.get(url, options)
      .then(response => response.data)
      .catch(() => {
        // if (error.response && error.response.status === 401)
          router.push('/login')
        // console.log("Error requesting post from backend", error)
      })
  }
  postLink(category, link) {
    console.log("add comment")
    const url = `/posts`;
    return axios.post(url, { "uri": link, "category": category }, options)
      .then(() => {router.push("/categories/" + category)})
      .catch((error) => {
        if (error.response && error.response.status === 401)
          router.push('/login')
        console.log("Error requesting post from backend", error)
      })
  }
  addComment(postId, comment) {
    console.log("add comment")
    const url = `/posts/${postId}`;
    return axios.post(url, { "text": comment}, options)
      .then(response => response.data)
      .catch((error) => {
        if (error.response && error.response.status === 401)
          router.push('/login')
      })
  }
  getUserProfile(userId) {
    console.log("get post by id")
    const url = `/users/${userId}`;
    return axios.get(url, options)
      .then(response => response.data)
      .catch((error) => {
        if (error.response && error.response.status === 401)
          router.push('/login')
        console.log("Error requesting post from backend", error)
      })
  }
  getPostsByUser(userId) {
    console.log("get post by user")
    const url = `/users/${userId}/posts`;
    return axios.get(url, options)
      .then(response => this.posts = response.data)
      .catch((error) => {
        if (error.response && error.response.status === 401)
          router.push('/login')
        console.log("Error requesting post from backend", error)
      })
  }
  getCommentsByUser(userId) {
    console.log("get post by user")
    const url = `/users/${userId}/comments`;
    return axios.get(url, options)
      .then(response => this.comments = response.data)
      .catch((error) => {
        if (error.response && error.response.status === 401)
          router.push('/login')
        console.log("Error requesting post from backend", error)
      })
  }
  getToken(username, password) {
    const url = `/tokens`;
    return axios.post(url, options, {
      auth: {
        username: username,
        password: password
      }})
      .then(response => {
        localStorage.token = response.data._id
        localStorage.username = response.data.user
        window.location.href = '/'
      })
      .catch((error) => {
        console.log("Error requesting token", error)
      })
  }
}
