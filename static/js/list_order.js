// 폼 & select 문을 선택해서 가져옴
const sortForm = document.getElementById('sort-form');
const sortSelect = document.getElementById('sort-select');

// 변화를 폼에 제출
sortSelect.addEventListener('change', function() {
  sortForm.submit();
});