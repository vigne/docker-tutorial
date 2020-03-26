<template>
  <div class="post-card">
    <div class="card">
      <div class="card-content">
        <h2 class="is-size-4 has-text-weight-bold">{{post.uri}}</h2>
        <small class="post-date">{{post.creation_date | formatDate}}</small>
        <small class="post-author">{{post.author_name}}</small>
        <small class="post-category">{{post.category}}</small>
        <small class="post-comments">Comments: {{post.comment_count}}</small>
      </div>
    </div>
  </div>
</template>
<script>
  import moment from 'moment'
  export default {
    props: [
      'post'
    ],
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
  .card {
    height: 100px;
    background-position: center;
    background-size: cover;
    text-align: center;
  }
  .card-content {
    padding-top: 5px;
    position: absolute;
    color: #FFF;
    background-color: #00d1b2;
    top: 0;
    padding: 10px;
    height: 100px;
    width: 100%;
    span {
      font-size: 18px;
      text-align: center;
      width: 100%;
      position: absolute;
      bottom: 10px;
      right: 0;
    }
    h2 {
      margin-top: 10px;
    }
  }
  .post-date {
    background-color: #151515;
    color: #FFF;
    font-size: .75em;
    padding: 2px 10px;
    position: absolute;
    top: 0;
    right: 0;
  }
  .post-author {
    background-color: #151515;
    color: #FFF;
    font-size: .75em;
    padding: 2px 10px;
    position: absolute;
    top: 0;
    left: 0;
  }
  .post-category {
    background-color: #151515;
    color: #FFF;
    font-size: .75em;
    padding: 2px 10px;
    position: absolute;
    bottom: 0;
    left: 0;
  }
  .post-comments {
    background-color: #151515;
    color: #FFF;
    font-size: .75em;
    padding: 2px 10px;
    position: absolute;
    bottom: 0;
    right: 0;
  }
</style>
