<template>
  <div class="category-card">
    <div class="card">
      <div class="card-content">
        <h2 class="is-size-4 has-text-weight-bold">{{category._id}}</h2>
        <h3 class="counter">{{category.count}}</h3>
      </div>
    </div>
  </div>
</template>
<script>
  import moment from 'moment'
  export default {
    props: [
      'category'
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
    background-image: url('https://placekitten.com/200/100');
    height: 100px;
    background-position: center;
    background-size: cover;
    text-align: center;
  }
  .card-content {
    padding-top: 50px;
    position: absolute;
    color: #FFF;
    background-color: rgba(0, 0, 0, 0.35);
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
  .counter {
    background-color: #151515;
    color: #FFF;
    /* font-size: .75em; */
    font-weight: bold;
    padding: 2px 10px;
    position: absolute;
    top: 0;
    right: 0;
  }
</style>
