// 버튼 요소들을 선택합니다.
const reviewButton = document.querySelector('.profile__user--review');
const bookmarkButton = document.querySelector('.profile__user--bookmark');
const likeButton = document.querySelector('.profile__user--like');
const followerButton = document.querySelector('.profile__user--followercount');
const followingButton = document.querySelector('.profile__user--followingcount');

// 컨텐츠 요소들을 선택합니다.
const content1 = document.querySelector('.profile__content1');
const content2 = document.querySelector('.profile__content2');
const content3 = document.querySelector('.profile__content3');
const content4 = document.querySelector('.profile__content4');
const content5 = document.querySelector('.profile__content5');

// 나의글 버튼을 클릭했을 때의 동작을 정의합니다.
reviewButton.addEventListener('click', () => {
  // 모든 컨텐츠를 숨깁니다.
  content1.style.display = 'none';
  content2.style.display = 'none';
  content3.style.display = 'none';
  content4.style.display = 'none';
  content5.style.display = 'none';

  // 모든 info 요소의 색상을 변경합니다.
  reviewButton.classList.remove('profile__user--infoactivebtn')
  bookmarkButton.classList.remove('profile__user--infoactivebtn')
  likeButton.classList.remove('profile__user--infoactivebtn')
  followerButton.classList.remove('profile__user--infoactivebtn')
  followingButton.classList.remove('profile__user--infoactivebtn')

  // 나의글 컨텐츠를 보여줍니다.
  content1.style.display = 'block';

  // 나의글 info 요소의 색상을 변경합니다.
  reviewButton.classList.add('profile__user--infoactivebtn')
});

// 북마크 버튼을 클릭했을 때의 동작을 정의합니다.
bookmarkButton.addEventListener('click', () => {
  // 모든 컨텐츠를 숨깁니다.
  content1.style.display = 'none';
  content2.style.display = 'none';
  content3.style.display = 'none';
  content4.style.display = 'none';
  content5.style.display = 'none';

  // 모든 info 요소의 색상을 변경합니다.
  reviewButton.classList.remove('profile__user--infoactivebtn')
  bookmarkButton.classList.remove('profile__user--infoactivebtn')
  likeButton.classList.remove('profile__user--infoactivebtn')
  followerButton.classList.remove('profile__user--infoactivebtn')
  followingButton.classList.remove('profile__user--infoactivebtn')

  // 북마크 컨텐츠를 보여줍니다.
  content2.style.display = 'block';

  // 북마크 info 요소의 색상을 변경합니다.
  bookmarkButton.classList.add('profile__user--infoactivebtn')
});

// 좋아요 버튼을 클릭했을 때의 동작을 정의합니다.
likeButton.addEventListener('click', () => {
  // 모든 컨텐츠를 숨깁니다.
  content1.style.display = 'none';
  content2.style.display = 'none';
  content3.style.display = 'none';
  content4.style.display = 'none';
  content5.style.display = 'none';

  // 모든 info 요소의 색상을 변경합니다.
  reviewButton.classList.remove('profile__user--infoactivebtn')
  bookmarkButton.classList.remove('profile__user--infoactivebtn')
  likeButton.classList.remove('profile__user--infoactivebtn')
  followerButton.classList.remove('profile__user--infoactivebtn')
  followingButton.classList.remove('profile__user--infoactivebtn')

  // 좋아요 컨텐츠를 보여줍니다.
  content3.style.display = 'block';

  // 좋아요 info 요소의 색상을 변경합니다.
  likeButton.classList.add('profile__user--infoactivebtn')
});

// 팔로워 버튼을 클릭했을 때의 동작을 정의합니다.
followerButton.addEventListener('click', () => {
  // 모든 컨텐츠를 숨깁니다.
  content1.style.display = 'none';
  content2.style.display = 'none';
  content3.style.display = 'none';
  content4.style.display = 'none';
  content5.style.display = 'none';

  // 모든 info 요소의 색상을 변경합니다.
  reviewButton.classList.remove('profile__user--infoactivebtn')
  bookmarkButton.classList.remove('profile__user--infoactivebtn')
  likeButton.classList.remove('profile__user--infoactivebtn')
  followerButton.classList.remove('profile__user--infoactivebtn')
  followingButton.classList.remove('profile__user--infoactivebtn')

  // 팔로워 컨텐츠를 보여줍니다.
  content4.style.display = 'block';

  // 팔로워 count 요소의 색상을 변경합니다.
  followerButton.classList.add('profile__user--infoactivebtn')
});

// 팔로윙 버튼을 클릭했을 때의 동작을 정의합니다.
followingButton.addEventListener('click', () => {
  // 모든 컨텐츠를 숨깁니다.
  content1.style.display = 'none';
  content2.style.display = 'none';
  content3.style.display = 'none';
  content4.style.display = 'none';
  content5.style.display = 'none';

  // 모든 info 요소의 색상을 변경합니다.
  reviewButton.classList.remove('profile__user--infoactivebtn')
  bookmarkButton.classList.remove('profile__user--infoactivebtn')
  likeButton.classList.remove('profile__user--infoactivebtn')
  followerButton.classList.remove('profile__user--infoactivebtn')
  followingButton.classList.remove('profile__user--infoactivebtn')

  // 팔로윙 컨텐츠를 보여줍니다.
  content5.style.display = 'block';

  // 팔로윙 count 요소의 색상을 변경합니다.
  followingButton.classList.add('profile__user--infoactivebtn')
});


const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// 팔로우 버튼 클릭 이벤트 리스너
const followBtn = document.getElementById('followBtn');
if (followBtn) {
  followBtn.addEventListener('click', () => {
    const personId = followBtn.getAttribute('data-person');
    axios.defaults.headers.common['X-CSRFToken'] = csrftoken;  // CSRF 토큰 설정
    axios.post(`/accounts/profile/${personId}/follow/`)
      .then((response) => {
        const isFollowed = response.data.is_followed
        // 서버로부터의 응답을 처리
        if (isFollowed == true) {
          // 팔로우 성공 시 동작
          followBtn.innerHTML = '<svg id="i-checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="18" height="18" fill="none" stroke="currentcolor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M2 20 L12 28 30 4" /></svg><p style="margin-left: 5px;">팔로잉</p>';
          followBtn.classList.remove('profile__user--followbtn')
          followBtn.classList.add('profile__user--unfollowbtn')
        } else {
          // 언팔로우 성공 시 동작
          followBtn.innerHTML = '<p>팔로우</p>';
          followBtn.classList.remove('profile__user--unfollowbtn')
          followBtn.classList.add('profile__user--followbtn')
        }

        const followingsCountTag = document.querySelector('#followings-count')
        const followersCountTag = document.querySelector('#followers-count')
    
        const followingsCountData = response.data.followings_count
        const followersCountData = response.data.followers_count
    
        followingsCountTag.textContent = ' ' + followingsCountData
        followersCountTag.textContent =  ' ' + followersCountData
      })

      .catch(error => {
        // 에러 처리
        console.error(error);
      });
  });
}

const followBtns2 = document.querySelectorAll('.followBtn2');
followBtns2.forEach(followBtn => {
  if (followBtn) {
    followBtn.addEventListener('click', () => {
      const personId = followBtn.getAttribute('data-person');
      axios.defaults.headers.common['X-CSRFToken'] = csrftoken;  // CSRF 토큰 설정
      axios.post(`/accounts/profile/${personId}/follow/`)
        .then((response) => {
          const isFollowed = response.data.is_followed
          // 서버로부터의 응답을 처리
          if (isFollowed == true) {
            // 팔로우 성공 시 동작
            followBtn.innerHTML = '<p>팔로잉</p>';
            followBtn.classList.remove('profile__follow--followbtn')
            followBtn.classList.add('profile__follow--unfollowbtn')
          } else {
            // 언팔로우 성공 시 동작
            followBtn.innerHTML = '<p>팔로우</p>';
            followBtn.classList.remove('profile__follow--unfollowbtn')
            followBtn.classList.add('profile__follow--followbtn')
          }
        })

        .catch(error => {
          // 에러 처리
          console.error(error);
        });
    });
  }
})

const followBtns3 = document.querySelectorAll('.followBtn3');
followBtns3.forEach(followBtn => {
  if (followBtn) {
    followBtn.addEventListener('click', () => {
      const personId = followBtn.getAttribute('data-person');
      axios.defaults.headers.common['X-CSRFToken'] = csrftoken;  // CSRF 토큰 설정
      axios.post(`/accounts/profile/${personId}/follow/`)
        .then((response) => {
          const isFollowed = response.data.is_followed
          // 서버로부터의 응답을 처리
          if (isFollowed == true) {
            // 팔로우 성공 시 동작
            followBtn.innerHTML = '<p>팔로잉</p>';
            followBtn.classList.remove('profile__follow--followbtn')
            followBtn.classList.add('profile__follow--unfollowbtn')
          } else {
            // 언팔로우 성공 시 동작
            followBtn.innerHTML = '<p>팔로우</p>';
            followBtn.classList.remove('profile__follow--unfollowbtn')
            followBtn.classList.add('profile__follow--followbtn')
          }
        })

        .catch(error => {
          // 에러 처리
          console.error(error);
        });
    });
  }
});