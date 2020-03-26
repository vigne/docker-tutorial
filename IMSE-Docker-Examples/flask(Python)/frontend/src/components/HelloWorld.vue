<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <button @click="handleButtonClick">ping the API</button>
    <p>{{payload.message}}</p>
    <p v-if="error_bool">{{helper}}</p>
    <p v-if="error_bool">{{error_msg}}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  methods: {
      handleButtonClick() {
        console.log("clicked button")
        this.error_bool = false
        axios.get('http://localhost:8000/helloworld')
        .then((response) => {
            this.payload = response.data
            console.log(response.data)
            this.clicked = "clicked"
      })
      .catch(error => {
          this.payload = {'message': "something went wrong! Your Api isn't running properly."}
          this.error_bool = true
          this.helper = "right click -> Inspect -> Console. Check the console error message after button click"
          this.error_msg = error
      })
    }
  },
  data(){
    return{
        payload: [],
        helper: "",
        error_msg: "",
        error_bool: null
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
