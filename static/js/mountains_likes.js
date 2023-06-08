const forms = document.querySelectorAll(".like-form");
const likeCsrftokenLike = document.querySelector("[name=csrfmiddlewaretoken]").value;

forms.forEach((form) => {
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    const mountainId = e.target.dataset.mountainId;
    axios({
      method: 'post',
      url: `/mountains/${mountainId}/likes/`,
      headers: {"X-CSRFToken" : likeCsrftokenLike},
    }).then((response) => {
      const isLiked = response.data.is_liked;
      const likeBtn = form.querySelector(`#like-btn`)
      console.log(isLiked)
      console.log(likeBtn)
      if (isLiked){
        likeBtn.className = "bi bi-heart-fill like__btn--style"
      } else {
        likeBtn.className = "bi bi-heart like__btn--style"
      }
      const likeCountData = response.data.like_count;
      const likeCountTag = form.closest('.max-w-sm').querySelector('.flex--row #like-count');
      likeCountTag.textContent = likeCountData
    })
    .catch((error) => {
      console.log(error.response)
    })
  })
})