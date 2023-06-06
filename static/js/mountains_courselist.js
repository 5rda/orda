const forms = document.querySelectorAll(".bookmark-form");
const bookmarkCsrftokenLike = document.querySelector("[name=csrfmiddlewaretoken]").value;

forms.forEach((form) => {
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    const courseId = e.target.dataset.courseId;
    const mountainId = e.target.dataset.mountainId;
    axios({
      method: 'POST',
      url: `/mountains/${mountainId}/course/${courseId}/bookmark/`,
      headers: {"X-CSRFToken" : bookmarkCsrftokenLike},
    }).then((response) => {
      const isBookmarked = response.data.is_bookmarked;
      const bookmarkBtn = form.querySelector(`#bookmark-btn-${courseId}`);
      console.log(isBookmarked)
      console.log(bookmarkBtn)
      if (isBookmarked){
        bookmarkBtn.className = 'bi bi-bookmark-fill bookmark--style';
      } else{
        bookmarkBtn.className = 'bi bi-bookmark bookmark--style';
      }
    })
    .catch((error) => {
      console.log(error.response)
    })
  })
})