<template>
  <div class="contact-us full-screen">
    <nav class="navbar navbar-ct-default" role="navigation-demo">
      <div class="container">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
          <img src="@/assets/img/icon.png" alt>
          <router-link :to="{path:'/'}" class="navbar-brand">Horizon Manager</router-link>
        </div>

        <!-- Collect the nav links, forms, and other content for toggling -->
        <div class="collapse navbar-collapse" id="navigation-example-2">
          <ul class="nav navbar-nav navbar-right">
            <li>
              <router-link :to="{path:'/'}">Home</router-link>
            </li>
          </ul>
        </div>
        <!-- /.navbar-collapse -->
      </div>
      <!-- /.container-->
    </nav>
    <div class="wrapper wrapper-full-page section content">
      <div class>
        <div class="container">
          <div class="row">
            <div class="col-md-8 col-md-offset-2 text-center">
              <h2 class="title text-danger">404 Not Found</h2>
              <h2 class="title">Oops! It seems that this page does not exist.</h2>
            </div>
          </div>
        </div>
      </div>
    </div>
    <footer class="footer-demo">
      <div class="container">
        <nav class="pull-left">
          <ul>
            <li>
              <router-link :to="{path:'/'}">Home</router-link>
            </li>
            <li>
              <router-link :to="{path:'/register'}">Register</router-link>
            </li>
          </ul>
        </nav>
      </div>
    </footer>
  </div>
</template>

<script>
export default {};
</script>
<style scoped>
img {
  height: 35px !important;
  margin-bottom: 2px;
}
nav {
  z-index: 1000;
}
</style>
