<script>
  export let location;

  const moveToHome = () => {
    window.location.hash = "/";
  };

  const moveToLogin = () => {
    window.location.hash = "/Login";
  };
</script>

<footer>
  <div class="footer-block">
    <div class="footer-icons" on:click={moveToHome}>
      {#if location === "home"}
        <img src="assets/home.svg" alt="" />
      {:else}
        <img src="assets/home2.svg" alt="" />
      {/if}
      <div class="footer-icons__img"></div>
      <div>홈</div>
    </div>
    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="assets/news.svg" alt="" />
      </div>
      <div>동네생활</div>
    </div>
    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="assets/location.svg" alt="" />
      </div>
      <div>내 근처</div>
    </div>
    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="assets/chat.svg" alt="" />
      </div>
      <div>채팅</div>
    </div>
    <div class="footer-icons" on:click={moveToLogin}>
      <div class="footer-icons__img">
        <img src="assets/user.svg" alt="" />
      </div>
      <div>로그인하기</div>
    </div>
  </div>
</footer>
