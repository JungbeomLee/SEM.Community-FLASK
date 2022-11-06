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
            console.log(data['useremail'])
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

function login() {
    const loginBtn = document.getElementById('login_btn');
    const form = document.getElementById('form');   

    loginBtn.addEventListener('click', (e) => {
        e.preventDefault(); // 기본 폼 동작 막기

        let loginId = document.getElementById('useremail').value;
        console.log(loginId)
        let password = document.getElementById('password').value;

        console.log(JSON.stringify({ loginId, password }))

        userLoginDataPost(loginId, password)
    });
}
