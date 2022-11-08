function getUserData() {
    fetch('/user/own_user/get', {
        method : 'GET'
    })
    .then(res => res.json())
    .then(data => {
        arrangeGetData(data)
    })
}

function arrangeGetData(data) {
    // 타이틀 설정
    document.getElementById('user_title').innerText = data['user_nickname'];
    // 프로필 이미지 링크 설정
    document.getElementById('profilePic').src = data['user_profile_image_link']
    // 이름 GET
    document.getElementById('user_name').innerText = data['user_name'];
    // 닉네임 GET
    document.getElementById('user_nickname').innerText = data['user_nickname'];
    // 자기소개 GET
    document.getElementById('user_profile').innerText = data['user_profile'];
    // 가입일자 GET
    document.getElementById('user_created_at').innerText = data['user_created_at'];
}

// 페이지가 로드될 경우 GET 요청
window.onload = getUserData();


