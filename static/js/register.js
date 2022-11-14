window.addEventListener("keyup", (e) => {
    if(e.code === "Enter") {
        document.getElementById("login_submit").click();
    }
})

const loginSubmit = document.getElementById('login_submit')
loginSubmit.addEventListener('click', (e) => {
    function login() {

        let userName = document.getElementById('username').value;
        let userNickName = document.getElementById('usernickname').value;
        let userEmail = document.getElementById('useremail').value;
        let password = document.getElementById('password').value;
        let rePassword = document.getElementById('re_password').value;
        let profile = document.getElementById('profile').value;
        let user_Data = new Object();

        user_Data.userName = userName;
        user_Data.userNickName = userNickName;
        user_Data.userEmail = userEmail;
        user_Data.password = password;
        user_Data.rePassword = rePassword;
        user_Data.profile = profile;

        checkFormInput(user_Data)
        userLoginDataPost(user_Data)
    };

    login();
});

function userLoginDataPost(user_Data) {
    let loginData = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'username' : user_Data['userName'],
            'usernickname' : user_Data['userNickName'],
            'useremail': user_Data['userEmail'],
            'password': user_Data['password'],
            're_password' : user_Data['rePassword'],
            'profile' : user_Data['profile']
        }),
        mode: 'no-cors'
    };
    fetch(`/register/post`, loginData)
        .then(res => res.json())
        .then(data => {
            if(data['post_data_check'] == true) {
                if(data['email_compare_check'] == true) {
                    alert('Already sign up email')
                }else {
                    if(data['signUp_check'] == true) {
                        alert('Sign up successed')
                        location.href='/'
                    }
                }
            }else {
                alert('Post date False')
            }
        })
}

function checkFormInput(user_Data){ 
    if(user_Data['userName'] == ''){
        alert('Please type your name')
        throw"stop";
    }else if(user_Data['userNickName'] == ''){
        alert('Please type your nickname')
        throw"stop";
    }else if(user_Data['userEmail'] == ''){
        alert('Please type your email')
        throw"stop";
    }else if(user_Data['password'] == ''){
        alert('Please type your password')
        throw"stop";
    }else if(user_Data['rePassword'] == ''){
        alert('Please type your rePassword')
        throw"stop";
    }else if(user_Data['profile'] == ''){
        alert('Please type your profile')
        throw"stop";
    }else {
        if(user_Data['password'] != user_Data['rePassword']){
            alert('Unmatch password')
            throw"stop";
        }
    }

}

