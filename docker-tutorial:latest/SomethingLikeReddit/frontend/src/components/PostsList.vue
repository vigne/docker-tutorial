<template>
  <div class="posts container">
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

  export default {
    name: 'PostsList',
    components : {
      PostCard
    },
    data () {
      return {
        posts: []
      }
    },
    methods: {
      getFeaturedPosts() {
        apiService.getFeaturedPosts().then((data) => this.posts = data)
      }
    },
    mounted() {
      this.getFeaturedPosts()
    }
  }
</script>
<style lang="scss" scoped>
  .posts {
    margin-top: 0px;
    text-align: center;
  }
</style>
