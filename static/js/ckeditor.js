ClassicEditor
.create(document.querySelector('#content'), {
  language: 'ko',
})
.then(editor => {
  editor.model.document.on('change:data', () => {
    document.querySelector('#content').value = editor.getData();
  });
})
.catch(error => {
  console.error(error);
});