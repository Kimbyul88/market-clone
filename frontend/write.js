const form = document.getElementById("write-form");

const handleSubmitForm = async (event) => {
  event.preventDefault();
  try {
    const formData = new FormData(form);

    const res = await fetch("/items", {
      //items는 데이터를 보내는 주소
      method: "POST",
      body: new FormData(form),
    });
    const data = await res.json(); //리턴한 값!

    if (data === "200") {
      window.location.pathname = "/";
    }
  } catch (e) {
    console.error(e);
  }
};

form.addEventListener("submit", handleSubmitForm);
