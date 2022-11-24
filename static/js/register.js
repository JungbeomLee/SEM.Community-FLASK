// detect usernickname input and check usernickname duplicate
const inputUsernickName = document.getElementById('usernickname')
inputUsernickName.addEventListener('input', (e) => {
    document.getElementById('nickname_duplicate_check_text').innerText = "Checking you nickname"
    function detectInputAndCheckDuplicate() {
        let userNickname = document.getElementById('usernickname').value;

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

        fetch(`/register/registerchecknickname`, changeData)
            .then(res => res.json())
            .then(data => {
                if (data['nickname_duplicate_check'] == 0) {
                    nickname_duplicate_check = 0;
                    document.getElementById('nickname_duplicate_check_text').innerText = "Already you using this nickname";
                } else if (data['nickname_duplicate_check'] == 1) {
                    nickname_duplicate_check = 1;
                    document.getElementById('nickname_duplicate_check_text').innerText = "You can use this nickname";
                } else {
                    nickname_duplicate_check = -1;
                    document.getElementById('nickname_duplicate_check_text').innerText = "You can't use this nickname";
                }
            });
    }

    setTimeout(detectInputAndCheckDuplicate, 1500)
})

// enter 감지
window.addEventListener("keyup", (e) => {
    if (e.code === "Enter") {
        document.getElementById("login_submit").click();
    }
})

// form 회원가입 input value 가져옴
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

// nickname 중복 검사 변수값 확인
function userLoginDataPost(user_Data) {
    if (nickname_duplicate_check != -1) {
        postRegisterData(user_Data)
    } else {
        alert("You can't use this nickname");
    }
}

// 회원가입 post 요청
function postRegisterData(user_Data) {
    let loginData = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'username': user_Data['userName'],
            'usernickname': user_Data['userNickName'],
            'useremail': user_Data['userEmail'],
            'password': user_Data['password'],
            're_password': user_Data['rePassword'],
            'profile': user_Data['profile']
        }),
        mode: 'no-cors'
    };
    fetch(`/register/post`, loginData)
        .then(res => res.json())
        .then(data => {
            if (data['post_data_check'] == true) {
                if (data['email_compare_check'] == true) {
                    alert('Already sign up email')
                } else {
                    if (data['signUp_check'] == true) {
                        alert('Sign up successed')
                        location.href = '/'
                    }
                }
            } else {
                alert('Post date False')
            }
        })
}

// input data 확인
function checkFormInput(user_Data) {
    if (user_Data['userName'] == '') {
        alert('Please type your name')
        throw "stop";
    } else if (user_Data['userNickName'] == '') {
        alert('Please type your nickname')
        throw "stop";
    } else if (user_Data['userEmail'] == '') {
        alert('Please type your email')
        throw "stop";
    } else if (user_Data['password'] == '') {
        alert('Please type your password')
        throw "stop";
    } else if (user_Data['rePassword'] == '') {
        alert('Please type your rePassword')
        throw "stop";
    } else if (user_Data['profile'] == '') {
        alert('Please type your profile')
        throw "stop";
    } else {
        if (user_Data['password'] != user_Data['rePassword']) {
            alert('Unmatch password')
            throw "stop";
        }
    }

}

