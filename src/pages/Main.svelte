<script>
  import { onMount } from "svelte";
  import Footer from "../components/Footer.svelte";
  import { getDatabase, ref, onValue } from "firebase/database";

  let min = new Date().getMinutes();
  let hour = new Date().getHours();
  let sec = new Date().getSeconds();
  let time = new Date().getTime();

  setInterval(
    () => (
      (time = time + 1000),
      (min = new Date(time).getMinutes()),
      (hour = new Date(time).getHours()),
      (sec = new Date(time).getSeconds())
    ),
    1000
  );

  //$: items라는 변수를 반응형으로 설정한다.!!!
  $: items = [];

  const calcTime = (timestamp) => {
    //한국시간 UTC+9
    const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
    const time = new Date(curTime - timestamp);
    const hour = time.getHours();
    const minute = time.getMinutes();
    const second = time.getSeconds();

    if (hour > 0) return `${hour}시간 전`;
    else if (minute > 0) return `${minute}분 전`;
    else if (second > 0) return `${second}초 전`;
    else return "방금 전";
  };

  const db = getDatabase();
  const itemsRef = ref(db, "items/");
  //itemsRef가 바뀔때 마다 스냅샷이 내려오게 되고, 스냅샷이 올때마다
  //업데이트 된다!!!!!!!!

  onMount(() =>
    onValue(itemsRef, (snapshot) => {
      const data = snapshot.val();
      items = Object.values(data).reverse();
    })
  );
</script>

<header>
  <div class="info-bar">
    <div class="info-bar__time">{hour}:{min}:{sec}</div>
    <div class="info-bar__icons">
      <img src="assets/chart-bar.svg" alt="chart-bar" />
      <img src="assets/wifi.svg" alt="wifi" />
      <img src="assets/battery.svg" alt="battery" />
    </div>
  </div>
  <div class="menu-bar">
    <div class="menu-bar__location">
      <span>역삼1동</span>
      <img src="assets/arrow.svg" alt="arrow" />
    </div>
    <div class="menu-bar__icons">
      <img src="assets/search.svg" alt="search" />
      <img src="assets/menu.svg" alt="menu" />
      <img src="assets/alert.svg" alt="alert" />
    </div>
  </div>
</header>
<main>
  {#each items as item}
    <div class="item-list">
      <div class="item-list__img">
        <img src={item.imgUrl} alt={item.title} />
      </div>
      <div class="item-list__info">
        <div class="item-list__info-title">{item.title}</div>
        <div class="item-list__info-meta">
          {item.place}
          {calcTime(item.insertAt)}
        </div>
        <div class="item-list__info-price">
          {item.price.toLocaleString("ko-KR") + "원"}
        </div>
        <div>{item.description}</div>
      </div>
    </div>
  {/each}
  <a class="write-btn" href="#/write">+ 글쓰기</a>
</main>
<Footer location="home" />
<div class="media-info-msg">화면 사이즈를 줄여주세요</div>

<style>
</style>
