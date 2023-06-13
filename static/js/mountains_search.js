$('document').ready(function() {
  var area0 = ["전국","서울특별시","인천광역시","대전광역시","광주광역시","대구광역시","울산광역시","부산광역시","경기도","강원도","충청북도","충청남도","전라북도","전라남도","경상북도","경상남도","제주도"];
  var area1 = ["전체"];
  var area2 = ["전체"];
  var area3 = ["전체"];
  var area4 = ["전체"];
  var area5 = ["전체"];
  var area6 = ["전체"];
  var area7 = ["전체"];
  var area8 = ["전체","고양시","과천시","광명시","광주시","구리시","군포시","김포시","남양주시","동두천시","부천시","성남시","수원시","시흥시","안산시","안성시","안양시","양주시","오산시","용인시","의왕시","의정부시","이천시","파주시","평택시","포천시","하남시","화성시","가평군","양평군","여주군","연천군"];
  var area9 = ["전체","강릉시","동해시","삼척시","속초시","원주시","춘천시","태백시","고성군","양구군","양양군","영월군","인제군","정선군","철원군","평창군","홍천군","화천군","횡성군"];
  var area10 = ["전체","제천시","청주시","충주시","괴산군","단양군","보은군","영동군","옥천군","음성군","증평군","진천군","청원군"];
  var area11 = ["전체","계룡시","공주시","논산시","보령시","서산시","아산시","천안시","금산군","당진군","부여군","서천군","연기군","예산군","청양군","태안군","홍성군"];
  var area12 = ["전체","군산시","김제시","남원시","익산시","전주시","정읍시","고창군","무주군","부안군","순창군","완주군","임실군","장수군","진안군"];
  var area13 = ["전체","광양시","나주시","목포시","순천시","여수시","강진군","고흥군","곡성군","구례군","담양군","무안군","보성군","신안군","영광군","영암군","완도군","장성군","장흥군","진도군","함평군","해남군","화순군"];
  var area14 = ["전체","경산시","경주시","구미시","김천시","문경시","상주시","안동시","영주시","영천시","포항시","고령군","군위군","봉화군","성주군","영덕군","영양군","예천군","울릉군","울진군","의성군","청도군","청송군","칠곡군"];
  var area15 = ["전체","거제시","김해시","마산시","밀양시","사천시","양산시","진주시","진해시","창원시","통영시","거창군","고성군","남해군","산청군","의령군","창녕군","하동군","함안군","함양군","합천군"];
  var area16 = ["전체","서귀포시","제주시","남제주군","북제주군"];
 
  
 
  // 시/도 선택 박스 초기화
 
  $("select[name^=sido]").each(function() {
   $selsido = $(this);
   $.each(eval(area0), function() {
    $selsido.append("<option value='"+this+"'>"+this+"</option>");
   });
   $selsido.next().append("<option value=''>구/군 선택</option>");
  });
 
  
 
  // 시/도 선택시 구/군 설정
 
  $("select[name^=sido]").change(function() {
  // var selectedSido = $(this).val();
  //  $("#hidden_sido2").val(selectedSido);

   var area = "area"+$("option",$(this)).index($("option:selected",$(this))); // 선택지역의 구군 Array
   var $gugun = $(this).next(); // 선택영역 군구 객체
   $("option",$gugun).remove(); // 구군 초기화
 
   if(area == "area0")
    $gugun.append("<option value=''>구/군 선택</option>");
   else {
    $.each(eval(area), function() {
     $gugun.append("<option value='"+this+"'>"+this+"</option>");
    });
   }
 });

//   $("select[name^=gugun]").change(function() {
//    var selectedGugun = $(this).val();
//    $("#hidden_gugun2").val(selectedGugun);
//  });
});

$(document).ready(function() {    
  $("select[name^=sido]").change(function() {
    var selectedSido = $(this).val();
    
    // 모든 이미지 숨기기
    $(".mountain__search--mapbox").hide();
    
    // 선택한 sido에 해당하는 이미지만 보이기
    $(".mountain__search--mapbox[data-sido='" + selectedSido + "']").show();

    $(".mountain__search--gugun").show();

    $(document).ready(function() {
      $("select[name^=gugun]").change(function() {
        var selectedGugun = $(this).val();

        if (selectedGugun === '전체') {
          // 전체 선택 시 모든 mountain__search--gugun 요소를 보이도록 설정
          $(".mountain__search--gugun").show();
        } else {
          // 선택한 gugun에 해당하는 mountain__search--gugun 요소만 보이도록 설정
          $(".mountain__search--gugun").hide();
          $(".mountain__search--gugun[data-gugun='" + selectedGugun + "']").show();
        }
      });
    });
  });
});

document.addEventListener('DOMContentLoaded', function() {
  var tagButtons = document.querySelectorAll('#review-tags label input');
  var selectedTagsContainer = document.getElementById('selected-tags');

  tagButtons.forEach(function(tagButton) {
    tagButton.addEventListener('click', function(event) {
      var label = this.parentElement;
      label.classList.toggle('selected');

      // 선택한 태그 목록 업데이트
      var selectedTags = document.querySelectorAll('#review-tags label.selected input');
      console.log(selectedTags)

      // 선택된 태그 목록 표시
      var selectedTagsArray = Array.from(selectedTags).map(function(input) {
        var inputName = '# ' + input.getAttribute('data-tag-name');
        return '<div class="mountain__reviewcrt--tag selected">' + inputName + '</div>';
      });

      // 선택된 태그들을 쉼표로 구분한 문자열로 설정하여 selectedTagsContainer 내에 업데이트
      selectedTagsContainer.innerHTML = selectedTagsArray.join(' ');
    });
  });
});

