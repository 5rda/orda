window.addEventListener('scroll', function() {
  var nav = document.getElementById('main-nav');
  var header = document.querySelector('header');
  var headerHeight = header.offsetHeight;

  if (window.pageYOffset >= headerHeight) {
    nav.style.top = '0'; 
  } else {
    nav.style.top = '-100px'; 
  }
});