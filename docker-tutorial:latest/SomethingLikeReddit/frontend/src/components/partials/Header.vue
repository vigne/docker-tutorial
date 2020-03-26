<template>

<section class="hero ">
  <div class="hero-body">
    <div class="container">
      <h1 class="title">
        Something Like Reddit
      </h1>
      <h2 class="subtitle">
        If it's ain't written here ... it ain't true!
      </h2>
    </div>
  </div>
</section>
</template>
<script>
export default {
  name: 'Header'
}
</script>
<style lang="scss" scoped>
.hero {
    text-align: center;
    background-image: url("https://cdn.pixabay.com/photo/2016/02/01/00/56/news-1172463_960_720.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
.hero-body .title {
    color: #cc0000;
    text-shadow: 4px 4px 4px rgba(0, 0, 0, 0.6);
    padding: 0px 0 10px;
    font-size: 60px;
}
.subtitle {
    color: #cc0000;
    text-shadow: 4px 4px 4px rgba(0, 0, 0, 0.7);
    font-size: 45px;
}
.is-xl {
    font-size: 1.7rem;
}

</style>
