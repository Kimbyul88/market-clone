<script>
  import Login from "./pages/Login.svelte";
  import Main from "./pages/Main.svelte";
  import Signup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import Router from "svelte-spa-router";
  import "./css/style.css";

  //자바스트립트 작성
  const routes = {
    "/": Main,
    "/login": Login,
    "/signup": Signup,
    "/write": Write,
    //"*":NotFound
  };
</script>

<Router {routes} />

<!--HTML-->
<main></main>

<!-- css작성! -->
<style>
</style>
