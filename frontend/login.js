const form = document.querySelector("#login-form");

//let accessToken = null;

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);

  const res = await fetch("/login", {
    method: "post",
    body: formData,
  });
  const data = await res.json(); //서버에서 가져온 응답을 json으로 바꿔줌.

  const accessToken = data.access_token;
  //console.log(accessToken);

  //로컬스토리지에 토큰을 저장하기!!
  window.localStorage.setItem("token", accessToken); //key(우리가 정하면 됨), value
  //세선 스토리지
  // window.sessionStorage.setItem("token", accessToken);
  alert("로그인되었습니다!!");

  // const infoDiv = document.querySelector("#info");
  // infoDiv.innerText = "로그인되었습니다!";

  window.location.pathname = "/";

  // const btn = document.createElement("button");
  // btn.innerText = "상품 가져오기";
  // btn.addEventListener("click", async () => {
  //   const res = await fetch("/items", {
  //     //서버님 items를 가져와 주세요
  //     headers: {
  //       //header에 엑세스토큰을 넣어서 인증을 한다.
  //       Authorization: `Bearer ${accessToken}`, //프리픽스 같은것...?
  //     },
  //   });
  //   const data = await res.json();
  //   console.log(data);
  // });
  // infoDiv.appendChild(btn);
};

form.addEventListener("submit", handleSubmit);
