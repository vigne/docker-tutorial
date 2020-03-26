<template>
<nav class="navbar container" role="navigation" aria-label="main navigation">
  <div id="navbar" class="navbar-menu">
    <div v-if="getUser()">
      <div class="navbar-start">
        <a class="button new">
          <router-link :to="'/post'" >
            New Post
          </router-link>
        </a>
        <a class="button is-dark">
          <router-link :to="'/'">
            <strong>Home</strong>
          </router-link>
        </a>
        <a class="button is-dark">
          <router-link to="/categories">
            <strong>Categories</strong>
          </router-link>
        </a>
        <a class="button is-dark">
          <router-link :to="'/profile/' + this.username" >
            Profile
          </router-link>
        </a>
      </div>
    </div>
    <div v-else>
      <div class="navbar-start">
        <a class="button is-dark">
          <router-link :to="'/login'">
            <strong>Sign In</strong>
          </router-link>
        </a>
      </div>
    </div>
  </div>
</nav>
</template>
<script>
export default {
  name: 'Nav',
  data() {
    return {
      username: ""
    }
  },
  methods: {
    getUser() {
      let username = localStorage.username
      console.log(username)
      if (username == undefined){
        console.log("not logged in")
        return false
      }
      this.username = username
      return username
    }
  },
}
</script>
<style lang="scss" scoped>
nav {
    margin-top: 25px;
    margin-bottom: 30px;
    a {
        font-weight: bold;
        color: #cc0000;
        &.router-link-exact-active {
            color: #d88d00;
        }
    }
}
.username {
  font-weight: bold;
  color: #cc0000;
}
.button {
  margin-right: 20px;
}
.new {
  margin-right: 100px;
}
</style>
