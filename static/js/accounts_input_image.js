const profileInput = document.querySelector('input[type="file"]');
const profilePreview = document.getElementById('profile-preview');

profileInput.addEventListener('change', function(event) {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function(e) {
    profilePreview.src = e.target.result;
    profilePreview.style.display = 'block';
  }

  reader.readAsDataURL(file);
});
