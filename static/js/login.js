function createCookie(value) {
    var now = new Date();
    var expirationDate = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 7, 0, 0, 0);

    document.cookie = 'token=' + value + '; expires=' + expirationDate + '; path=/';
};
$.ajax({
    method: "POST",
    url: "http://localhost:8000/login",
    data: JSON.stringify({
        "email": id,
        "password": password
    }),
    contentType: 'application/json'
})
.done(function (msg) {
    // 요청 전송 후 토큰이 존재하는 경우 토큰을 쿠키에 저장함
    if (msg.access_token) {
        createCookie(msg.access_token);
    }
});