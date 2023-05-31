$(window).scroll(function(){
  if ($(this).scrollTop() > 300){
    $('.btn__gotop').show();
  } else{
    $('.btn__gotop').hide();
  }
});
$('.btn__gotop').click(function(){
  $('html, body').animate({scrollTop:0},400);
  return false;
});