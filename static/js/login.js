const loginSubmit = document.getElementById('login_submit')
loginSubmit.addEventListener('click', (e) => {
    function login() {
        e.preventDefault(); // 기본 폼 동작 막기

    let loginId = document.getElementById('useremail').value;
    let password = document.getElementById('password').value;

    userLoginDataPost(loginId, password)
    };

    login();
});

function userLoginDataPost(loginId, password) {
    let loginData = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'useremail': loginId,
            'password': password
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