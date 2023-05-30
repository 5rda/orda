$(window).scroll(function(){
  if ($(this).scrollTop() > 300){
    $('.btn_gotop').show();
  } else{
    $('.btn_gotop').hide();
  }
});
$('.btn_gotop').click(function(){
  $('html, body').animate({scrollTop:0},400);
  return false;
});