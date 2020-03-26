<template>
  <div class="profile">
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container profile">
          <h1 class="title">
            {{ profile.name }} ({{ profile._id }})
          </h1>
        </div>
      </div>
    </section>
    <div class="mailto">
        <div class="label">mail:</div>
        <a :href="'mailto://' + profile.mail">{{ profile.mail }}</a>
    </div>
    <div class="address">
        <div class="label">Address</div>
        <pre>{{ profile.address }}</pre>
    </div>
    <div class="follows">
        <div class="label">Follows</div>
        <ul>
          <li v-for="(category, idx) in profile.follows" :key="idx">
            {{ category }}
          </li>
        </ul>
    </div>

    <div class="posts">
      <div class="label">
        Authored Posts<br/>
        <div v-if="this.posts.length == 0">
          <a class="button is-dark submit" v-on:click="getPosts()">
            <strong>Load posts</strong>
          </a>
        </div>
      </div>
      <div v-for="(post, idx) in posts" :key="idx" :index="posts._id" class="column is-full">
        <router-link :to="'/posts/' + post._id">
          <PostCard :post="post" />
        </router-link>
      </div>
    </div>

    <div>
      <div class="label">
        Authored Comments<br/>
        <div v-if="this.comments.length == 0">
          <a class="button is-dark submit" v-on:click="getComments()">
            <strong>Load comments</strong>
          </a>
        </div>
      </div>
      <div  class="comments">
        <div v-for="(comment, idx) in comments" :key="idx" :index="comment._id" class="column">
          <table>
            <tr><td><b>{{comment.creation_date | formatDate}}</b> <a :href="'/posts/' + comment._id">[Got to post]</a></td></tr>
            <tr><td>{{comment.text}}</td></tr>
          </table>
        </div>
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
    name: 'PostSingle',
    data () {
      return {
        profile: {},
        comments: [],
        posts: []
      }
    },
    components : {
      PostCard
    },
    methods: {
      getUserProfile() {
        apiService.getUserProfile(this.$route.params.id)
          .then((data) => this.profile = data)
          .catch((err) => {console.log("ProfileView", err)})
      },
      getComments() {
        console.log("load comments")
        apiService.getCommentsByUser(this.$route.params.id)
          .then((data) => {this.comments = data===undefined ? [] : data})
          .catch((err) => {console.log("ProfileView", err)})
      },
      getPosts() {
        console.log("load posts")
        apiService.getPostsByUser(this.$route.params.id)
          .then((data) => {this.posts = data===undefined ? [] : data})
          .catch((err) => {console.log("ProfileView", err)})
      }
    },
    filters: {
      formatDate: function (value) {
        if (!value) return ''
        value = moment(value).format('DD.MM.YYYY hh:mm')
        return value
      }
    },
    created() {
      this.user = this.getUserProfile();
    }
  }
</script>
<style lang="scss" scoped>
  .comments div:nth-child(odd) {
        background-color: #00d1b2;
  }
</style>
