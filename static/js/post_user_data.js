document.write('<script src="upload_user_image_popup.js')

function getUserData(password) {
    let check = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'password': password
        }),
        mode: 'no-cors'
    };

    fetch(`/user/own_user/post`, check)
        .then(res => res.json())
        .then(data => {arrangeGetData(data)})
}



function arrangePostData(data) {
    // 유저 데이터 변경을 위한 비밀번호 입력 확인
    // 입력 안했을 경우
    if(data['password_check'] == false) {
        // 타이틀 설정
        document.getElementById('user_title').innerText = data['user_nickname'];
        // 프로필 이미지 링크 설정
        document.getElementById('profilePic').src = data['user_profile_image_link']
        // 이름 GET
        document.getElementById('user_name').innerText = data['user_name'];
        // 닉네임 GET
        document.getElementById('user_nickname').innerText = data['user_name'];
        // 자기소개 GET
        document.getElementById('user_profile').innerText = data['user_name'];
        // 가입일자 GET
        document.getElementById('user_created_at').innerText = data['user_name'];
    // 입력 했을 경우
    }else if(password_check == true) {
        // 이미지 링크 설정
        document.getElementById('profilePic').src = data['user_profile_image_link']
        // 프로필 이미지 유무 확인
        if(data['check_user_profile_image_name_check'] = false) {
            // 프로필 이미지 없을경우
            document.getElementById('user_image_label').innerHTML = '<label onclick="openPopup_no_profile_image_pass();" for="newProfilePhoto" class="upload-file-block"><div class="text-center"><div class="mb-2"><i class="fa fa-camera fa-2x"></i></div><div class="text-uppercase">Update <br /> Profile Photo</div></div></label>'
        }else {
            // 프로필 이미지 있을경우
            document.getElementById('user_image_label').innerHTML = '<label onclick="openPopup_have_profile_image();" for="newProfilePhoto" class="upload-file-block"><div class="text-center"><div class="mb-2"><i class="fa fa-camera fa-2x"></i></div><div class="text-uppercase">Update <br /> Profile Photo</div></div></label>'
        }
        // 이름 
        

    }

}

window.onload = getUserData();


