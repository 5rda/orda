  function loadKakaoMapScript(callback) {
    if (window.kakao) {
        // 이미 카카오맵 API가 로드되어 있는 경우
        callback();
    } else {
        // 카카오맵 API 로드
        var script = document.createElement("script");
        script.type = "text/javascript";
        script.src = "https://dapi.kakao.com/v2/maps/sdk.js?appkey=d39fcd60ffdc96ae99454337f5e45a16&libraries=services&autoload=false";
        document.head.appendChild(script);
        
        script.onload = function () {
            kakao.maps.load(function () {
                callback();
            });
        };
    }
  }

  // 카카오맵 초기화 함수
  function initMap(modal_courseId, courseInfo) {
    var container = document.getElementById('map-' + modal_courseId);
    var options = {
      center: new kakao.maps.LatLng(37.5665, 126.9780), 
      level: 7
    };
    var map = new kakao.maps.Map(container, options);

    var linePath = [];
    var linePath = courseInfo.features[0].geometry.coordinates.map(function(coordinate) {
      var x = coordinate[0];
      var y = coordinate[1];
      return new kakao.maps.LatLng(y, x);
    });


    // 출발 마커 이미지
    var startMarkerPosition = linePath[0];
    var startMarkerImage = new kakao.maps.MarkerImage(
      '/static/img/icons/start.png',
      new kakao.maps.Size(100, 100),
      { offset: new kakao.maps.Point(50, 80) }
      );
    // 출발 좌표에 마커 표시
    var startMarker = new kakao.maps.Marker({
      position: startMarkerPosition,
      map: map,
      title: "출발지",
      image: startMarkerImage
    });

    // 도착 마커 이미지
    var endMarkerPosition = linePath[0];
    var endMarkerImage = new kakao.maps.MarkerImage(
      '/static/img/icons/end.png',
      new kakao.maps.Size(100, 100),
      { offset: new kakao.maps.Point(50, 80) }
      );
    var endMarkerPosition = linePath[linePath.length - 1];
    // 도착 좌표에 마커 표시
    var endMarker = new kakao.maps.Marker({
      position: endMarkerPosition,
      map: map,
      title: "도착지",
      image: endMarkerImage
    });

    // 줌 리모컨
    var zoomControl = new kakao.maps.ZoomControl();
    map.addControl(zoomControl, kakao.maps.ControlPosition.LEFT);  

        
    // 중간 인덱스 계산
    var middleIndex = Math.floor(linePath.length / 2);
    var center = linePath[middleIndex];

    // Polyline을 이용하여 선 그리기
    var polyline = new kakao.maps.Polyline({
      path: linePath, // linePath에 저장된 좌표들로 설정
      strokeWeight: 3,
      strokeColor: '#FF0000',
      strokeOpacity: 0.7,
      strokeStyle: 'solid'
    });
    polyline.setMap(map);

    // 부드럽게 마커가 위치한 곳으로 이동합니다
    map.panTo(center);
  };

  // 북마크 비동기
  const forms = document.querySelectorAll(".bookmark-form");
  const bookmarkCsrftokenLike = document.querySelector("[name=csrfmiddlewaretoken]").value;

  forms.forEach((form) => {
  form.addEventListener('submit', function(e) {
  e.preventDefault();
  const courseId = e.target.dataset.courseId;
  const mountainId = e.target.dataset.mountainId;
  axios({
    method: 'POST',
    url: `/mountains/${mountainId}/course/${courseId}/bookmark/`,
    headers: {"X-CSRFToken" : bookmarkCsrftokenLike},
  }).then((response) => {
    const isBookmarked = response.data.is_bookmarked;
    const bookmarkBtn = form.querySelector(`#bookmark-btn-${courseId}`);
    if (isBookmarked){
      bookmarkBtn.className = 'bi bi-bookmark-fill btn--spot';
    } else{
      bookmarkBtn.className = 'bi bi-bookmark btn--spot';
    }
  })
  .catch((error) => {
    console.log(error.response)
  })
  })
  })