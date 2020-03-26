<template>
  <div class="categories">
    <section class="hero is-primary">
      <!-- <div class="hero-body">
        <div class="container profile">
          <h1 class="title">
            Categories Overview
          </h1>
        </div>
      </div> -->

    </section>
    <div class="columns is-multiline">
      <div v-for="(category, idx) in categories" :category="category" :key="idx" :index="category._id" class="column is-one-quarter">
        <router-link :to="'/categories/' + category._id">
          <CategoryCard :category="category" />
        </router-link>
      </div>
    </div>
  </div>
</template>
<script>
  import moment from 'moment'

  import {APIService} from '../APIServices';
  const apiService = new APIService();
  import CategoryCard from '@/components/CategoryCard';

  export default {
    name: 'Categories',
    data () {
      return {
        categories: {}
      }
    },
    components : {
      CategoryCard
    },

    methods: {
      getCategories() {
        apiService.getCategories()
          .then((data) => this.categories = data)
          .catch((err) => {console.log("CategoriesView", err)})
      },
    },
    filters: {
      formatDate: function (value) {
        if (!value) return ''
        value = moment(value).format('DD.MM.YYYY hh:mm')
        return value
      }
    },
    created() {
      this.user = this.getCategories();
    }
  }
</script>
<style lang="scss" scoped>
</style>
