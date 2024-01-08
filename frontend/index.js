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

const renderData = (data) => {
  //data = [{id:1,title:'aaa'},{id:2...}....]
  const main = document.querySelector("main");

  data.reverse();
  data.forEach(async (obj) => {
    console.log(obj);

    const div = document.createElement("div");
    div.className = "item-list";

    const ImgDiv = document.createElement("div");
    ImgDiv.className = "item-list__img";

    const img = document.createElement("img");
    const res = await fetch(`/images/${obj.id}`);
    const blob = await res.blob(); //이미지를 BLOB타입으로.
    const url = URL.createObjectURL(blob);
    img.src = url;

    const InfoDiv = document.createElement("div");
    InfoDiv.className = "item-list__info";

    const InfoTitleDiv = document.createElement("div");
    InfoTitleDiv.className = "item-list__info-title";
    InfoTitleDiv.innerText = obj.title;

    const InfoMetaDiv = document.createElement("div");
    InfoMetaDiv.className = "item-list__info-meta";
    InfoMetaDiv.innerText = obj.place + " " + calcTime(obj.insertAt);

    const InfoPriceDiv = document.createElement("div");
    InfoPriceDiv.className = "item-list__info-price";
    InfoPriceDiv.innerText = obj.price.toLocaleString("ko-KR") + "원";

    ImgDiv.appendChild(img);

    InfoDiv.appendChild(InfoTitleDiv);
    InfoDiv.appendChild(InfoMetaDiv);
    InfoDiv.appendChild(InfoPriceDiv);

    div.appendChild(ImgDiv);
    div.appendChild(InfoDiv);

    main.appendChild(div);
  });
};

const fetchList = async () => {
  const accessToken = window.localStorage.getItem("token");
  console.log(accessToken);
  const res = await fetch("/items", {
    //     //서버님 items를 가져와 주세요
    headers: {
      //       //header에 엑세스토큰을 넣어서 인증을 한다.
      Authorization: `Bearer ${accessToken}`, //프리픽스 같은것...?
    },
  });
  if (res.status === 401) {
    alert(accessToken);
    window.location.pathname = "/login.html";
  }
  const data = await res.json(); // 서버에서 받은 데이터
  renderData(data);
};

fetchList();
