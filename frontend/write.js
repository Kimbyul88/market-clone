const form = document.getElementById("write-form");
const headerArrow = document.querySelector(".write-header__left");

const handleSubmitForm = async (event) => {
  event.preventDefault();
  const body = new FormData(form);
  body.append("insertAt", new Date().getTime());
  try {
    const res = await fetch("/items", {
      //items는 데이터를 보내는 주소
      method: "POST",
      body, // body:body와 같음!
    });
    const data = await res.json(); //리턴한 값!

    if (data === "200") {
      window.location.pathname = "/";
    }
  } catch (e) {
    console.error(e);
  }
};

const handlePrev = () => {
  window.location.pathname = "/";
};

form.addEventListener("submit", handleSubmitForm);
headerArrow.addEventListener("click", handlePrev);
