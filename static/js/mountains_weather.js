document.addEventListener('DOMContentLoaded', function() {
  var buttons = document.querySelectorAll('[id^="btn-"]');
  var contents = document.querySelectorAll('[id^="weather-"]');
  
  // 첫 번째 내용 보여주기
  if (contents.length > 0) {
      contents[0].style.display = 'block';
      buttons[0].parentNode.classList.add('selected--btn');
  }

  buttons.forEach(function(button) {
      button.addEventListener('click', function() {
          var targetId = this.id.substring(4);  // 버튼 ID에서 'btn-'을 제외한 부분을 추출
          var targetContent = document.getElementById('weather-' + targetId);

          // 모든 내용 숨기기
          contents.forEach(function(content) {
              content.style.display = 'none';
          });

          // 모든 버튼의 클래스 제거
          buttons.forEach(function(btn) {
              btn.parentNode.classList.remove('selected--btn');
          });

          // 선택한 내용 보여주기
          targetContent.style.display = 'block';

          // 선택한 버튼에 클래스 추가
          this.parentNode.classList.add('selected--btn');

          // 선택한 내용의 이미지 보여주기
          var targetImages = targetContent.querySelectorAll('img');
          targetImages.forEach(function(image) {
              image.style.display = 'block';
          });
      });
  });
});