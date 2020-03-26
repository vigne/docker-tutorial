<template>
  <div class="post-new">
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container post">
          <h1 class="title">
            Author new post
          </h1>
        </div>
      </div>
    </section>
    <section class="new-post">
        <span class="label">Category:</span>
        <input type="text" v-model="category" maxlength="255" size="40"/><br/>
        <span class="label">Link:</span>
        <input type="text" v-model="link" maxlength="1024" size="100"/><br/><br/>
        <a class="button is-dark submit" v-on:click="postLink()" type="submit">
          <strong>Post</strong>
        </a>

    </section>
  </div>
</template>
<script>
  import {APIService} from '../APIServices';
  const apiService = new APIService();

  export default {
    name: 'NewPost',
    data () {
      return {
        link: "",
        category: ""
      }
    },
    methods: {
      postLink() {
        if(this.category == '')
          return
          if(this.link == '')
            return
        apiService.postLink(this.category, this.link)
          .then((data) => console.log(data))
          .catch((err) => {console.log("NewPostView", err)})
      }
    }
  }
</script>
<style lang="scss" scoped>

</style>
