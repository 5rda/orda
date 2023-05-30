const formFields = document.querySelectorAll('.form__field input, .form__field textarea');

formFields.forEach(function(field) {
  const clearButton = document.createElement('button');
  clearButton.className = 'clear-button';
  clearButton.type = 'button';
  clearButton.innerText = 'X';
  clearButton.style.display = 'none';
  clearButton.style.color = 'var(--sub-color)';
  clearButton.style.right = '0';
  field.parentNode.appendChild(clearButton);

  clearButton.addEventListener('click', function() {
    field.value = '';
    clearButton.style.display = 'none';
  });

  field.addEventListener('input', function() {
    if (field.value.length > 0) {
      clearButton.style.display = 'inline-block';
    } else {
      clearButton.style.display = 'none';
    }
  });
});