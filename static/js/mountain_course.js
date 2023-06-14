

function loadKakaoMapScript(callback) {
  if (window.kakao) {
      // 이미 카카오맵 API가 로드되어 있는 경우
      callback();
  } else {
      // 카카오맵 API 로드
      const API_KEY = config.apikey;
      var script = document.createElement("script");
      script.type = "text/javascript";
      script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${API_KEY}&libraries=services&autoload=false`;
      document.head.appendChild(script);
      
      script.onload = function () {
          kakao.maps.load(function () {
              callback();
          });
      };
  }
}


function toggleWaypoints(courseId) {
  var checkbox = document.getElementById('waypoint-checkbox-' + courseId);
  var mapInfo = mapList[courseId];

  if (mapInfo && mapInfo.waypoints) {
    var waypoints = mapInfo.waypoints;

    if (checkbox.checked) {
      // 체크박스가 선택된 경우, 모든 경유지 마커를 표시합니다.
      for (var i = 0; i < waypoints.length; i++) {
        waypoints[i].setMap(mapInfo.map);
      }
    } else {
      // 체크박스가 선택되지 않은 경우, 모든 경유지 마커를 숨깁니다.
      for (var i = 0; i < waypoints.length; i++) {
        waypoints[i].setMap(null);
      }
    }
  }
}

// 페이지 로드 시 경유지 체크박스를 선택한 상태로 초기화합니다.
document.addEventListener("DOMContentLoaded", function() {
  var checkboxes = document.querySelectorAll("[id^='waypoint-checkbox-']");
  checkboxes.forEach(function(checkbox) {
    checkbox.checked = true; // 체크박스를 선택한 상태로 설정합니다.
    var courseId = checkbox.id.split("-")[2];
    toggleWaypoints(courseId); // 체크박스의 변경에 따라 경유지를 표시하거나 숨깁니다.
  });
});

// 카카오맵 초기화 함수
function initMap(courseId, courseInfo, courseDetail) {
  var container = document.getElementById('map-' + courseId);
  var options = {
    center: new kakao.maps.LatLng(37.5665, 126.9780), 
    level: 6
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

  // courseDetail의 마커 추가
  var detail = courseDetail.features
  var courseWaypoints = [];

  detail.forEach(function(feature) {
    var geometry = feature.geometry;
    var properties = feature.properties;

    const forbiddenWords = ['계단', '길', '바위', '자연경관', '계곡', '나무', '쉼터', '흙', '하봉', '중봉', '고목', '관광', '전망대', '등산로 입구'];
    const regexPattern = new RegExp(forbiddenWords.join('|'), 'i');

    if (
      geometry.type === 'Point' &&
      ['PEAK', 'CULTURAL', 'ENTRY', 'SCENERY'].includes(properties.waypoint_category) &&
      !regexPattern.test(properties.waypoint_name)
    ) {
      var coordinates = geometry.coordinates;
      var markerPosition = new kakao.maps.LatLng(coordinates[1], coordinates[0]);

      var imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png";
      var imageSize = new kakao.maps.Size(16, 24); 
      var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);

      var marker = new kakao.maps.Marker({
        position: markerPosition,
        map: map,
        title: properties.waypoint_name,
        image: markerImage,
      });

      courseWaypoints.push(marker);
    }
  });


  // 부드럽게 마커가 위치한 곳으로 이동합니다
  map.panTo(center);

  // 코스별 지도 정보를 저장합니다.
  mapList[courseId] = {
    map: map,
    waypoints: courseWaypoints
  };
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