// navbar 버튼 색깔 변경
document.getElementById("탐색").addEventListener("click", function() {
  setButtonColor("탐색");
});

document.getElementById("등산로").addEventListener("click", function() {
  setButtonColor("등산로");
});

document.getElementById("마이코스").addEventListener("click", function() {
  setButtonColor("마이코스");
});

document.getElementById("인증샷").addEventListener("click", function() {
  setButtonColor("인증샷");
});


document.getElementById("로그인").addEventListener("click", function() {
  setButtonColor("로그인");
});

document.getElementById("회원가입").addEventListener("click", function() {
  setButtonColor("회원가입");
});

// document.getElementById("마이페이지").addEventListener("click", function() {
//   setButtonColor("마이페이지");
// });

// document.getElementById("로그아웃").addEventListener("click", function() {
//   setButtonColor("로그아웃");
// });

function setButtonColor(activeButtonId) {
  var buttonIds = ["탐색", "마이코스", "등산로", "인증샷", "로그인", "회원가입"];
  var activeColor = '#A2E04E';
  var inactiveColor = '#000000';

  buttonIds.forEach(function(buttonId) {
    var button = document.getElementById(buttonId);
    button.classList.remove("active-button"); // 기존의 active-button 클래스 제거

    if (buttonId === activeButtonId) {
      button.classList.add("active-button"); // 클릭한 버튼에 active-button 클래스 추가
    }

    button.addEventListener("mouseover", function() {
      if (buttonId !== activeButtonId) {
        button.style.color = activeColor;
      }
    });

    button.addEventListener("mouseout", function() {
      if (buttonId !== activeButtonId) {
        button.style.color = inactiveColor;
      }
    });
  });
}