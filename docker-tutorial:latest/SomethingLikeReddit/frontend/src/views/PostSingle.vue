<template>
  <div class="post-single">
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container post">
          <span class="meta"><b>{{post.author_name}}</b> posted at <b>{{post.creation_date | formatDate}}</b></span>
          <br/><br/>
          <h1 class="title">
            {{ post.uri }}
          </h1>
          <span class="comments_count"><b>{{getCount()}}</b> user commented on this post</span>
        </div>
      </div>
    </section>
    <section class="new-comment">
        <textarea v-model="comment" placeholder="Write comment here"></textarea>
        <a class="button is-dark submit" v-on:click="postComment()" type="submit">
          <strong>Comment</strong>
        </a>
    </section>
    <section class="post-comments">
      <div class="container comment">
          <div v-for="(comment, idx) in getComments()" :key="idx" class="column">
            <table>
              <tr>
                <td class="meta">
                  <b>{{comment.author_name}}</b> said at <b>{{comment.creation_date | formatDate}}</b>
                </td>
              </tr>
              <tr>
                  <td class="text">
                    {{comment.text}}
                  </td>
              </tr>
            </table>
            <br/>
          </div>
      </div>
    </section>
  </div>
</template>
<script>
  import {APIService} from '../APIServices';
  const apiService = new APIService();
  import moment from 'moment'
  export default {
    name: 'PostSingle',
    data () {
      return {
        post: {},
        comment: ""
      }
    },
    methods: {
      getPostById() {
        apiService.getPostById(this.$route.params.id)
          .then((data) => this.post = data)
          .catch((err) => {console.log("SingleView", err)})
      },
      getCount() {
        if(this.post.comments == undefined)
          return 0
        return this.post.comments.length
      },
      getComments() {
        if(this.post.comments == undefined)
          return []
        return this.post.comments
      },
      postComment() {
        console.log(this.comment)
        console.log(this.$route.params.id)
        var postId = this.$route.params.id
        apiService.addComment(this.$route.params.id, this.comment)
          .then(() => {
            apiService.getPostById(postId)
              .then((data) => {
                if(data != undefined)
                  this.post = data
              })
              .catch((err) => {console.log("SingleView", err)})
            return {}
          })
          .catch((err) => {console.log("SingleView", err)})
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
      this.getPostById();
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
