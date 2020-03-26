<template>
  <div class="category container">
    <div class="columns is-multiline">
      <div v-for="(post, idx) in posts" :post="post" :key="idx" :index="post._id" class="column is-full">
        <router-link :to="'/posts/' + post._id">
          <PostCard :post="post" />
        </router-link>
      </div>
    </div>
  </div>
</template>
<script>
  import {APIService} from '../APIServices';
  const apiService = new APIService();

  import PostCard from '@/components/PostCard';

  import moment from 'moment'
  export default {
    name: 'category',
    components : {
      PostCard
    },
    data () {
      return {
        posts: []
      }
    },
    methods: {
      getPostByCategory() {
        apiService.getPostByCategory(this.$route.params.id)
          .then((data) => this.posts = data)
          .catch((err) => {console.log("CategoryView", err)})
      }
    },
    mounted() {
      this.getPostByCategory()
    },
    filters: {
      formatDate: function (value) {
        if (!value) return ''
        value = moment(value).format('DD.MM.YYYY hh:mm')
        return value
      }
    }
  }
</script>
<style lang="scss" scoped>
  .comment > div:nth-child(even) {
    /* background-color: #d1d1e0; */
    background-color: #00d1b2;
  }
  .comment-date {
    background-color: #151515;
    color: #FFF;
    font-size: .75em;
    padding: 2px 10px;
    position: absolute;
    top: 0;
    right: 0;
  }
  .comment-author {
    background-color: #151515;
    color: #FFF;
    font-size: .75em;
    padding: 2px 10px;
    position: absolute;
    top: 0;
    left: 0;
  }
  .meta {
    padding-bottom: 10px;
  }
  .new-comment textarea {
    width: 90%;
    height: 100px;
    margin: 30px;
    margin-bottom: 0px;
  }
  .new-comment .submit {
    width: 90%;
    height: 40px;
    text-align: center;
    margin: 30px;
    margin-top: 0px;
  }
</style>
