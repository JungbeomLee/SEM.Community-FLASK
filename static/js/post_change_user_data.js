const postUserDataSubmit = document.getElementById('change_user_data_submit')
postUserDataSubmit.addEventListener('click', (e) => {
    function changeUserData() {
        e.preventDefault(); // 기본 폼 동작 막기
        let userNickname = document.getElementById('change_nickname').value;
        let userProfile = document.getElementById('change_profile').value;
        
        let user_Data = new Object();

        user_Data.userNickname = userNickname;
        user_Data.userProfile = userProfile;

        postChangeUserData(user_Data)
    };

    changeUserData()
})

function postChangeUserData(user_Data) {
    let changeData = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'user_nickname': user_Data['userNickname'],
            'user_profile' : user_Data['userProfile']
        }),
        mode: 'no-cors'
    };
    fetch(`/user/own_user/changedatapost`, changeData)
        .then(res => res.json())
        .then(data => {
            if(data['update'] == true) {
                alert('Success to update user data')
                window.location.reload();
            }else{
                alert('Failed to update user data')
                window.location.reload();
            }
        });
}




