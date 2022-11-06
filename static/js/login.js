function login() {
    const loginBtn = document.getElementById('login_btn');
    const form = document.getElementById('form');

    loginBtn.addEventListener('click', (e) => {
        e.preventDefault(); // 기본 폼 동작 막기

        let loginId = document.getElementById('useremail').value;
        console.log(loginId)
        let password = document.getElementById('password').value;

        console.log(JSON.stringify({ loginId, password }))
        
        let loginData = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'useremail': loginId,
                'password' : password
            }),
            mode : 'no-cors'
        };
            fetch(`/login/post`, loginData)
            .then((res) => console.log('response', res))
            .then((json) => {
                console.log(json);
            })
    });
}