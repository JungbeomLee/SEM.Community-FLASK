let nickname_duplicate_check = 2;

const nickNameDuplicateBtn = document.getElementById('nickname_duplicate_check_button')
nickNameDuplicateBtn.addEventListener('click', (e) => {
    e.preventDefault(); // 기본 폼 동작 막기
    let userNickname = document.getElementById('usernickname').value;

    if (userNickname == '') {
        alert('Please type your nickname')
        return "stop";
    }

    let changeData = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'user_nickname': userNickname,
        }),
        mode: 'no-cors'
    };
    fetch(`/user/own_user/ownuserchecknickname`, changeData)
        .then(res => res.json())
        .then(data => {
            if (data['nickname_duplicate_check'] == 0) {
                nickname_duplicate_check = 0;
                document.getElementById('nickname_duplicate_check_text').innerText = "Already you using this nickname";
            }else if (data['nickname_duplicate_check'] == 1){
                nickname_duplicate_check = 1;
                document.getElementById('nickname_duplicate_check_text').innerText = "You can use this nickname";
            }else {
                nickname_duplicate_check = -1;
                document.getElementById('nickname_duplicate_check_text').innerText = "You can't use this nickname";
            }
        });
})

const postUserDataSubmit = document.getElementById('change_user_data_submit')
postUserDataSubmit.addEventListener('click', (e) => {
    e.preventDefault(); // 기본 폼 동작 막기
    if (nickname_duplicate_check == 2){
        alert('You have to check your nickname duplicate')
        return"stop"
    }else {
        if (nickname_duplicate_check != -1) {
            function changeUserData() {
                let userNickname = document.getElementById('usernickname').value;
                let userProfile = document.getElementById('change_profile').value;
        
                if (userNickname == '') {
                    alert('Please type your nickname')
                    return "stop";
        
                } else if (userProfile == '') {
                    alter('Please type your profile text')
                    return "stop";
        
                };
        
        
                let user_Data = new Object();
        
                user_Data.userNickname = userNickname;
                user_Data.userProfile = userProfile;
        
                postChangeUserData(user_Data)
            };
        
            changeUserData()
        }else {
            alert("You can't use this nickname");
        }
    }
    
})

function postChangeUserData(user_Data) {
    let changeData = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'user_nickname': user_Data['userNickname'],
            'user_profile': user_Data['userProfile']
        }),
        mode: 'no-cors'
    };
    fetch(`/user/own_user/changedatapost`, changeData)
        .then(res => res.json())
        .then(data => {
            if (data['update'] == true) {
                alert('Success to update user data')
                window.location.reload();
            } else {
                alert('Failed to update user data')
                window.location.reload();
            }
        });
}
