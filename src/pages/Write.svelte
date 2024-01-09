<script>
  import { getDatabase, ref, push } from "firebase/database";
  import Footer from "../components/Footer.svelte";
  import {
    getStorage,
    ref as refImage,
    uploadBytes,
    getDownloadURL,
  } from "firebase/storage";

  let title;
  let price;
  let description;
  let place;
  let files;

  const db = getDatabase();
  const storage = getStorage();

  function writeUserData(imgUrl) {
    push(ref(db, "items/"), {
      title,
      price,
      description,
      place,
      insertAt: new Date().getTime(),
      imgUrl,
    });
    alert("글쓰기가 완료되었습니다");
    window.location.hash = "/";
  }

  const storageRef = refImage(storage, "/imgs");

  // // 'file' comes from the Blob or File API
  // uploadBytes(storageRef, file).then((snapshot) => {
  //   console.log("Uploaded a blob or file!");
  // });

  //$: if (files) console.log(files); //files가 바뀔때마다 콘솔로그가 찍힌다.
  const uploadFile = async () => {
    const file = files[0];
    const name = file.name;
    const imgRef = refImage(storage, name);
    await uploadBytes(imgRef, file);
    const url = await getDownloadURL(imgRef);
    return url;
  };

  const handleSubmit = async () => {
    const url = await uploadFile();
    console.log(url);
    writeUserData(url);
  };
</script>

<!-- <button on:click={() => console.log(title, price, description, place)}
  >test</button
> -->
<div class="write-header" id="write-header">
  <div class="write-header__left">
    <img src="assets/arrow2.svg" alt="" />
  </div>
  <div class="write-header__center">중고거래 글쓰기</div>
  <div class="write-header__right"></div>
</div>
<!--write-header-->
<form id="write-form" on:submit|preventDefault={handleSubmit}>
  <div>
    <label for="image">이미지</label>
    <input type="file" bind:files id="image" name="image" />
  </div>
  <div>
    <label for="title">제목</label>
    <input
      type="text"
      id="title"
      name="title"
      placeholder="제목을 입력해주세요"
      bind:value={title}
    />
  </div>
  <div>
    <label for="price">가격</label>
    <input
      type="number"
      id="price"
      name="price"
      placeholder="가격을 입력해주세요"
      bind:value={price}
    />
  </div>
  <div>
    <label for="description">설명</label>
    <input
      type="text"
      id="description"
      name="description"
      placeholder="상품에 대한 설명을 입력해주세요"
      bind:value={description}
    />
  </div>
  <div>
    <label for="place">장소</label>
    <input
      type="text"
      id="place"
      name="place"
      placeholder="거래 가능 장소를 입력해주세요"
      bind:value={place}
    />
  </div>
  <div class="submit-btn"><button type="submit">완료</button></div>
</form>
<Footer location="write" />

<style>
  .submit-btn button {
    border: 1px solid #c8c8c8;
    color: #f67a33;
    cursor: pointer;
  }
</style>
