
const uploadButton = document.querySelector('.upload-btn')
const uploadIcon = document.querySelector('.upload-icon')
const spinner = document.querySelector('.spinner')
const fileInput = document.getElementById('file-input')

uploadButton.addEventListener('click', function() {
  fileInput.click();
});

var myHeaders = new Headers();
myHeaders.append("Authorization", `Bearer ${accessToken}`);

var formdata = new FormData();
formdata.append("album", album);
formdata.append("type", "file");
formdata.append("name", "Gallery App");
formdata.append("title", "Gallery App");
formdata.append("description", "Uploaded by Imgur API");

var requestOptions = {
method: 'POST',
headers: myHeaders,
body: formdata,
redirect: 'follow'
};

fileInput.addEventListener('change', function() {
  uploadButton.setAttribute("disabled", "true");
  uploadIcon.style.display = "none";
  spinner.style.display = "block";
  
  formdata.append(file_type, fileInput.files[0]);
  fetch(`https://api.imgur.com/3/${postType}`, requestOptions)
    .then(response => response.json())
    .then(result => setPostUrl(result))
    .catch(error => console.log('error', error))
    .finally(() => {
      uploadButton.removeAttribute("disabled");
      uploadIcon.style.display = "flex";
      spinner.style.display = "none";
    })
});

var input_image = document.getElementById('id_image')
var uploaded_image = document.querySelector('.uploaded-image')

function setPostUrl(result) {
  if (result.success) {
    if (file_type == 'video') {
      setVideoUrl(result);
    } else {
      setPhotoUrl(result);
    }
  } else console.log(result);
};

function setPhotoUrl(result) {
  const post_link = result.data.link;
  uploaded_image.setAttribute('src', post_link);
  input_image.value = post_link;
};

function setVideoUrl(result) {
  const post_link = result.data.link;

  addToAlbum(result.data.id)
  .then(response => {
    if (response.success) {
      setTimeout(function() {
        setVideoAtr()
        input_image.value = post_link;
      }, 1000);
    }
  })

  uploaded_image.setAttribute('src', post_link);
};

function addToAlbum(videoId) {
  var headersAlbum = new Headers();
  headersAlbum.append("Authorization", `Bearer ${accessToken}`);

  var formDataAlbum = new FormData();
  formDataAlbum.append("ids[]", videoId);

  var requestOptionsAlbum = {
    method: 'POST',
    headers: headersAlbum,
    body: formDataAlbum,
    redirect: 'follow'
  };

  return fetch(`https://api.imgur.com/3/album/${album}/add`, requestOptionsAlbum)
    .then(response => response.json())
    .catch(error => {console.log('error', error);}
  );
};

function setVideoAtr() {
  let newVideo = document.querySelector('video')
  newVideo.setAttribute('preload', 'metadata')
  newVideo.setAttribute('controls', '');
  newVideo.load();
};
