const loginSubmit = document.getElementById('login_submit')
loginSubmit.addEventListener('click', (e) => {
    function login() {
        e.preventDefault(); // 기본 폼 동작 막기

    let userEmail = document.getElementById('useremail').value;
    let password = document.getElementById('password').value;
    
    let user_Data = new Object();

    
    user_Data.userEmail = userEmail;
    user_Data.password = password;

    userLoginDataPost(user_Data);
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
            'useremail': user_Data['userEmail'],
            'password': user_Data['password']
        }),
        mode: 'no-cors'
    };
    fetch(`/login/post`, loginData)
        .then(res => res.json())
        .then(data => {
            if(data['login'] == true) {
                document.cookie = "access_token="+data["access_token"]
                document.cookie = "refresh_token="+data["refresh_token"]
                location.href='/'
                alert('Success to login')
            }else{
                alert('Failed to login')
            }
        })
}

function checkFormInput(user_Data){ 
    if(user_Data['userEmail'] == ''){
        alert('Please type your email')
        throw"stop";
    }else if(user_Data['password'] == ''){
        alert('Please type your password')
        throw"stop";
    }

}