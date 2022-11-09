const passwordSubmit = document.getElementById('password_submit')
passwordSubmit.addEventListener('click', (e) => {
    function password() {
        e.preventDefault(); // 기본 폼 동작 막기
        let password = document.getElementById('password').value;

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

        getUserData(check)
    };

    password()
})

function getUserData(check) {
    fetch(`/user/own_user/post`, check)
        .then(res => res.json())
        .then(data => { arrangePostData(data) })
}

function arrangePostData(data) {
    // 유저 데이터 변경을 위한 비밀번호 입력 확인
    // 입력한 비밀번호가 일치할 경우
    if (data['password_check'] == true) {
        // 타이틀 설정
        document.getElementById('user_title').innerText = data['user_nickname'];
        // 타이틀 설정
        document.getElementById('user_name').innerText = data['user_name'];
        // 이미지 링크 설정
        document.getElementById('profilePic').src = data['user_profile_image_link']
        // 프로필 이미지 유무 확인
        if (data['check_user_profile_image_name_check'] = false) {
            // 프로필 이미지 없을경우 openPopup_no_profile_image_pass(); 넣기
            document.getElementById('user_image_label').innerHTML = '<label onclick="openPopup_no_profile_image_pass();" for="newProfilePhoto" class="upload-file-block"><div class="text-center"><div class="mb-2"><i class="fa fa-camera fa-2x"></i></div><div class="text-uppercase">Update <br /> Profile Photo</div></div></label>'
        } else {
            // 프로필 이미지 있을경우 openPopup_have_profile_image(); 넣기
            document.getElementById('user_image_label').innerHTML = '<label onclick="openPopup_have_profile_image();" for="newProfilePhoto" class="upload-file-block"><div class="text-center"><div class="mb-2"><i class="fa fa-camera fa-2x"></i></div><div class="text-uppercase">Update <br /> Profile Photo</div></div></label>'
        }
        // 수정 가능한 데이터 입력 form
        document.getElementById('form_input_change_user_data_div').innerHTML = '<div class="form-group"><input type="text" class="form-control" id="change_nickname" value="" placeholder="닉네임" name="change_nickname" required /></div><div class="form-group"><label for="change_profile"></label><input type="text" class="form-control" id="change_profile" value="" placeholder="자기소개" name="change_profile" required /></div><button type="submit" class="btn btn-primary">확인</button></form>'
        // 닉네임 기존값 넣기 
        document.getElementById('change_nickname').value = data['user_nickname']
        // 자기소개 기존값 넣기
        document.getElementById('change_profile').value = data['user_profile']
    }

}


