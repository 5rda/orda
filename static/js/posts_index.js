var postGrid = document.getElementById('postGrid');
var loadMoreBtn = document.getElementById('loadMoreBtn');
var page = 1;
var perPage = 12; 

function showMorePosts() {
  var hiddenPosts = postGrid.querySelectorAll('.post-item.hidden');
  var i = 0;

  while (i < perPage && hiddenPosts[i]) {
    hiddenPosts[i].classList.remove('hidden');
    i++;
  }

  if (hiddenPosts.length <= perPage) {
    loadMoreBtn.style.display = 'none';
  }
}

loadMoreBtn.addEventListener('click', showMorePosts);

var allPosts = postGrid.querySelectorAll('.post-item');
allPosts.forEach(function(post, index) {
  if (index >= perPage) {
    post.classList.add('hidden');
  }
});

if (allPosts.length <= perPage) {
  loadMoreBtn.style.display = 'none';
}

// 좋아요 비동기
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// 좋아요 버튼 클릭 이벤트 리스너
const postlikeBtns = document.querySelectorAll('.postindex__post--like');

if (postlikeBtns) {
  postlikeBtns.forEach((postlikeBtn) => {
    postlikeBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const postId = postlikeBtn.getAttribute('data-post');
      axios.defaults.headers.common['X-CSRFToken'] = csrftoken;  // CSRF 토큰 설정
      axios.post(`/posts/${postId}/likes/`)
        .then((response) => {
          const isliked = response.data.is_liked
          // 서버로부터의 응답을 처리
          if (isliked == true) {
            // 좋아요 성공 시 동작
            postlikeBtn.innerHTML = '<svg id="i-heart" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32" fill="#FFB6C1" stroke="#FFB6C1" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M4 16 C1 12 2 6 7 4 12 2 15 6 16 8 17 6 21 2 26 4 31 6 31 12 28 16 25 20 16 28 16 28 16 28 7 20 4 16 Z" /></svg>';
          } else {
            // 좋아요 취소 성공 시 동작
            postlikeBtn.innerHTML = '<svg id="i-heart" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32" fill="#DBDBDB" stroke="#FFB6C1" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M4 16 C1 12 2 6 7 4 12 2 15 6 16 8 17 6 21 2 26 4 31 6 31 12 28 16 25 20 16 28 16 28 16 28 7 20 4 16 Z" /></svg>';
          }

          const likesCountTags = document.querySelectorAll('.postindex__post--likecount')
          likesCountTags.forEach((likesCountTag) => {
            const likeId = likesCountTag.getAttribute('data-like');
            if (postId === likeId) {
              const likesCountData = response.data.likes_count
          
              likesCountTag.textContent = '좋아요' + ' ' + likesCountData
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
    margin: 20, // 아이템 간의 간격
    nav: true, // 네비게이션 버튼 표시 여부
    navText: ["<", ">"],
    dots: true, // 도트 표시 여부
    responsive: {
      // 반응형 옵션 설정
      0: {
        items: 1 // 0px 이상일 때, 1개의 아이템 표시
      },
      768: {
        items: 2 // 768px 이상일 때, 2개의 아이템 표시
      },
      1080: {
        items: 4 // 1080px 이상일 때, 4개의 아이템 표시
      }
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