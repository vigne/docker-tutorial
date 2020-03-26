<template>
  <div class="hello">
    <div>
        <h1>{{ msg }}</h1>
        <button v-if=!db_bool @click=handleButtonClick>init DB</button>
        <p>{{payload.message}}</p>
    </div>
    <div v-if=db_bool>
        <h2 class="center-align">Add a Student to Database</h2>
        <form @submit.prevent="register" >
        <div class="row">
            <div class="input-field">
                <label class="active" >Name </label>
                <input id="name" placeholder="firstname lastname" type="text" class="validate" v-model="name">
            </div>
        </div>
        <div class="row">
            <div class="input-field">
                <label class="active" >Grade </label>
                <input type="number" placeholder="1-5" class="validate" v-model="grade">
            </div>
        </div>
        <div>
            <div class="input-button">
                <button>insert</button>
            </div>
        </div>
        </form>
    </div>
    <div class="table" v-if=db_bool>
        <table class="table table-striped center-align">
            <tbody>
                <tr v-for="(student,i) in students" :key="i">
                <th scope="row">{{ student.first_name }}</th>  
                <th scope="row">{{ student.last_name}}</th> 
                <th>{{ student.grade }}</th>  
                </tr>
            </tbody>
        </table>
    </div>
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
        console.log("clicked init")
        this.db_bool = false
        axios.get('http://localhost:8000/initdb.php')
        .then((response) => {
            this.payload = response.data
            console.log(response.data)
            this.db_bool = true
            this.name = null
            this.grade = null
            this.getStudents()
        })
    },
    register(){
        console.log("clicked insert")
        let data = this.name.split(" ")
        axios.post('http://localhost:8000/student/post.php', {
            "first_name": data[0],
            "last_name": data[1],
            "grade": this.grade
        })
        .then((response) => {
            console.log(response.data)
            this.name = ""
            this.grade = ""
            this.getStudents()
        },(error) => {
        console.log(error);
        })
    },
    getStudents(){
        axios.get('http://localhost:8000/student/get.php')
        .then((response) => {
            this.students = response.data
            console.log(response.data)
        })
    }
  },
  data(){
    return{
        name: null,
        grade: null,
        payload: [],
        students: [],
        db_bool: null
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
.table {
    display: flex;
    align-items: center;
    justify-content: center;
    padding-top: 10px;
}
</style>
