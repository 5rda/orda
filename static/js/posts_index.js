document.addEventListener("DOMContentLoaded", function () {
  var loadMoreBtn = document.getElementById("loadMoreBtn");
  var postGrid = document.getElementById("postGrid");
  var posts = document.querySelectorAll(".post-item");

  var visiblePosts = 12; // 초기에 보여줄 게시물 수
  var increment = 12; // 더 보기 버튼을 누를 때 추가로 보여줄 게시물 수

  // 초기에 보여줄 게시물 수 이상일 경우 더 보기 버튼을 표시
  if (posts.length > visiblePosts) {
    loadMoreBtn.style.display = "block";
  }

  // 초기에 보여줄 게시물 수 이후의 게시물은 숨김
  for (var i = visiblePosts; i < posts.length; i++) {
    posts[i].style.display = "none";
  }

  // 더 보기 버튼 클릭 시 게시물 추가 보여주기
  loadMoreBtn.addEventListener("click", function () {
    var nextVisiblePosts = visiblePosts + increment;

    // 추가로 보여줄 게시물이 남아있을 경우 보여주기
    for (var i = visiblePosts; i < posts.length && i < nextVisiblePosts; i++) {
      posts[i].style.display = "block";
    }

    visiblePosts = nextVisiblePosts;

    // 모든 게시물을 보여준 경우 더 보기 버튼 숨김
    if (visiblePosts >= posts.length) {
      loadMoreBtn.style.display = "none";
    }
  });
});

// 좋아요 비동기
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// 좋아요 버튼 클릭 이벤트 리스너
const forms = document.querySelectorAll('.postindex__post--like');

if (forms) {
  forms.forEach((form) => {
    form.addEventListener('click', (e) => {
      e.preventDefault();
      const postId = form.getAttribute('data-post');
      axios.defaults.headers.common['X-CSRFToken'] = csrftoken;  // CSRF 토큰 설정
      axios.post(`/posts/${postId}/likes/`)
        .then((response) => {
          const isliked = response.data.is_liked
          const postlikeBtn = form.querySelector(`#postlike-btn`)
          // 서버로부터의 응답을 처리
          if (isliked == true) {
            // 좋아요 성공 시 동작
            postlikeBtn.className = 'bi bi-heart-fill like__btn--style';
          } else {
            // 좋아요 취소 성공 시 동작
            postlikeBtn.className = 'bi bi-heart like__btn--style';
          }

          const likesCountTags = document.querySelectorAll('.postindex__post--likecount')
          likesCountTags.forEach((likesCountTag) => {
            const likeId = likesCountTag.getAttribute('data-like');
            if (postId === likeId) {
              const likesCountData = response.data.like_count
              likesCountTag.textContent = likesCountData
            }
          });
        })

        .catch(error => {
          // 에러 처리
          console.error(error);
        });
    });
  });
}

$(document).ready(function() {
  $(".owl-carousel").owlCarousel({
    // OwlCarousel 옵션 설정
    items: 4, // 한 번에 표시할 아이템 수
    loop: false, // 무한 루프 여부
    margin: 10, // 아이템 간의 간격
    dots: true, // 도트 표시 여부
    animateIn: 'fadeIn',
    autoplay: true,
    rewind: true,
    autoplayTimeout: 3000,
    smartSpeed: 500,
    responsive: {
      // 반응형 옵션 설정
      0: {
        items: 1 // 0px 이상일 때, 1개의 아이템 표시
      },
      720: {
        items: 2
      },
      1080: {
        items: 3
      },
      1280: {
        items: 4
      },
    }
  });
});


// const page_elements = document.getElementsByClassName('page-link')
// Array.from(page_elements).forEach(function(element) {
//   element.addEventListener('click', function(event) {
//     event.preventDefault();
//     document.getElementById('page').value = this.dataset.page;
//     document.getElementById('searchForm').submit();
//   });
// });

// const btn_search = document.getElementById('btn_search');
// btn_search.addEventListener('click', function() {
//   document.getElementById('query').value = document.getElementById('search_query').value;
//   document.getElementById('page').value = 1;
//   document.getElementById('searchForm').submit();
// })