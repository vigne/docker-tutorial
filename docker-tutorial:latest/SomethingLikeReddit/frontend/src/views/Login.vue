<template>
    <div id="login">
      <div class="info">
        The defualt user is: <strong>ralph</strong> and it's password is <strong>pwd</strong>
        If the DB isn't initialized yet, click <a v-on:click="init()">here</a>
      </div>
        <input type="text" name="username" v-model="input.username" placeholder="Username" />
        <br/>
        <input type="password" name="password" v-model="input.password" placeholder="Password" />
        <br/>
        <a class="button is-dark submit" v-on:click="login()" type="submit">
          <strong>Login</strong>
        </a>
    </div>
</template>

<script>
  import {APIService} from '../APIServices';
  const apiService = new APIService();
  

  export default {
    name: 'Login',
    data() {
      return {
        input: {
          username: "",
          password: ""
        }
      }
    },
    methods: {
      login() {
        apiService.getToken(this.input.username, this.input.password)
      },
      init() {
        apiService.init()
      }
    }
  }
</script>

<style scoped>
    #login {
        text-align: center;
        margin: auto;
        margin-top: 20px;
        padding: 20px;
    }
</style>
