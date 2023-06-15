const commentSection = document.getElementById('comment-section');
const commentBtn = document.getElementById('go-comment-section')

commentBtn.addEventListener('click', function(event) {
  event.preventDefault();

  // 댓글 Y축을 가져온다
  const commentSectionOffsetTop = commentSection.offsetTop;

  window.scrollTo({
    top: commentSectionOffsetTop, 
    behavior: 'smooth'
  })
}) 


// ajax
// post liked
const forms = document.querySelectorAll(".like-form");
const postCsrftokenLike = document.querySelector("[name=csrfmiddlewaretoken]").value;

forms.forEach((form) => {
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    const postId = e.target.dataset.postId;
    axios({
      method: 'post',
      url: `/posts/${postId}/likes/`,
      headers: {"X-CSRFToken" : postCsrftokenLike},
    }).then((response) => {
      const isLiked = response.data.is_liked;
      const likeBtn = form.querySelector(`#like-btn`);
      if (isLiked){
        likeBtn.className = 'like__btn--style bi bi-heart-fill heart--color like__hover icon--size';
      } else{
        likeBtn.className = 'like__btn--style bi bi-heart like__hover icon--size';
      }
      const likeCountTag = form.querySelector('#like-count')
      const likeCountData = response.data.like_count
      likeCountTag.textContent = likeCountData
    })
    .catch((error) => {
      console.log(error.response)
    })
  })
})


// comment 좋아요
const commentLikeForms = document.querySelectorAll('.comment-like-form');
const clcsrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
commentLikeForms.forEach(form => {
  form.addEventListener('submit', function (event) {  
    event.preventDefault()
    const postId = event.target.dataset.postId;
    const commentId = event.target.dataset.commentId;
    axios({
      method: 'post',
      url: `/posts/${postId}/comments/${commentId}/comment_likes/`,
      headers: {'X-CSRFToken': clcsrfToken},
    }).then((response) => {
      const isLiked = response.data.cl_is_liked
      // console.log(isLiked)
      const likeBtn = document.querySelector(`#like-${commentId}`)
      const dislikeBtn = document.querySelector(`#dislike-${commentId}`)
      if (isLiked){
        likeBtn.className = "bi bi-hand-thumbs-up-fill like__hover text-primary";
        dislikeBtn.disabled = true;
      } else {
        likeBtn.className = "bi bi-hand-thumbs-up like__hover";
        dislikeBtn.disabled = false;}
      const likesCountData = response.data.cl_likes_count
      console.log(likesCountData) 
      const likesCountTag = document.querySelector(`#cl_likes_count_${commentId}`)
      console.log(likesCountTag)
      likesCountTag.textContent = likesCountData

      // location.reload();
    })
    .catch((error) => {
      console.error(response.data);
    });
  });
});
;


// comment 싫어요
const commentDislikeForms = document.querySelectorAll('.comment-dislike-form');
const cdcsrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
commentDislikeForms.forEach(form => {
  form.addEventListener('submit', function (event) {  
    event.preventDefault()
    const postId = event.target.dataset.postId;
    const commentId = event.target.dataset.commentId;
    const commentItem = document.querySelector(`#comment-content-${commentId}`);
    console.log(commentItem)
    axios({
      method: 'post',
      url: `/posts/${postId}/comments/${commentId}/comment_dislikes/`,
      headers: {'X-CSRFToken': cdcsrfToken},
    }).then((response) => {
      const isLiked = response.data.cd_is_liked
      // console.log(isLiked)
      const dislikeBtn = document.querySelector(`#dislike-${commentId}`)
      const likesBtn = document.querySelector(`#like-${commentId}`)
      if (isLiked){
        dislikeBtn.className = "bi bi-hand-thumbs-down-fill text-danger like__hover";
        likesBtn.disabled = true;
      } else {
        dislikeBtn.className = "bi bi-hand-thumbs-down like__hover";
        likesBtn.disabled = false;}
      const dislikesCountData = response.data.cd_likes_count
      console.log(dislikesCountData) 
      const dislikesCountTag = document.querySelector(`#cd_likes_count_${commentId}`)
      console.log(dislikesCountTag)
      dislikesCountTag.textContent = dislikesCountData
      
      const commentToggleBtn = document.querySelector(`#comment-toggle-${commentId}`);
      console.log(`#comment-toggle-${commentId}`)
      console.log(document.querySelector(`#comment-toggle-${commentId}`))

      if (dislikesCountData >= 10) {
        commentItem.style.display = "none"; // 댓글 숨기기
        // commentItem.textContent =  commentToggleBtn.textContent;
        commentToggleBtn.style.display = "block";
      } else {
        commentItem.style.display = "block"; // 댓글 보이기
        commentToggleBtn.style.display = "none";
      }
    })
    .catch((error) => {
      console.error(response.data);
    });
  });
});
;

// 싫어요 많은 댓글 보기
const commentToggleBtns = document.querySelectorAll('.comment-toggle-btn');

commentToggleBtns.forEach((btn) => {
  btn.addEventListener('click', function() {
    const commentId = btn.getAttribute('data-comment-id');
    const commentContent = document.querySelector(`#comment-content-${commentId}`);

    if (commentContent) {
      commentContent.style.display="block";
      btn.style.display = "none";
    }
  });
});

        


// // 댓글 등록 (미구현)
const commentForm = document.querySelector('.comment-form');
const commentList = document.querySelector('.comment-list');
const commentCountTag = document.querySelector('#post_comments');

commentForm.addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(commentForm);

    axios({
        method: 'post',
        url: commentForm.getAttribute('action'),
        data: formData,
        headers: {'X-Requested-With': 'XMLHttpRequest'},
    })
        .then(function(response) {
            location.reload();
            const newComment = response.data;

            // 새로운 댓글을 동적으로 추가하는 예시
            const commentItem = document.createElement('li');
            commentItem.textContent = newComment.content;
            commentList.appendChild(commentItem);

            // 댓글 입력 필드 초기화
            commentForm.reset();

            // 댓글 수 업데이트
            const commentCountData = response.data.post_comments;
            commentCountTag.textContent = commentCountData;
        })
        .catch(function(error) {
            console.log(error.response.data);
        });
});

       


// 댓글 삭제 
const deleteBtns = document.querySelectorAll('.delete-comment-btn');
deleteBtns.forEach((btn) => {
    btn.addEventListener('click', function (event) {
        event.preventDefault();

        const postId = event.target.dataset.postId;
        const commentId = btn.dataset.commentId;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        var deleteWarning = confirm('댓글을 삭제하시겠습니까?');
        
        if (deleteWarning) {
            axios({
                method: 'post',
                url: `/posts/${postId}/comments/${commentId}/delete/`,
                headers: { 'X-CSRFToken': csrfToken },
            })
                .then((response) => {
                    const status = response.data.status;
                    if (status === 'ok') {
                        const commentItem = document.querySelector(`#comment-${commentId}`);
                        if (commentItem) {
                            commentItem.remove();
                            const commentCountTag = document.querySelector(`#post_comments`)
                            const commentCountData = response.data.post_comments
                            commentCountTag.textContent = commentCountData
                        }
                    } else {
                    }
                })
                .catch((error) => {
                    console.log(error.response.data);
                });
        }
    });
});



// 팔로우
const form = document.querySelector("#follow-form")
const followcsrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value

form.addEventListener("submit", function (event) {
  event.preventDefault()

  const userId = event.target.dataset.userId;

  axios({
    method: "post",
    url: `/accounts/profile/${userId}/follow/`,
    headers: { "X-CSRFToken": followcsrftoken },
  }).then((response) => {
    const isFollowed = response.data.is_followed
    const followBtn = document.querySelector('#follow-form > input[type=submit]')

    if(isFollowed){
      followBtn.value='팔로우 취소'
    } else{
      followBtn.value='팔로우'
    }
  });
});