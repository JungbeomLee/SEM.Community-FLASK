function getUserData() {
    fetch('/user/own_user/get', {
        method : 'GET'
    })
    .then(res => res.json())
    .then(data => {
        arrangeGetData(data)
    })
}
function arrangeGetData(data) {
    console.log(data)
    // 타이틀 설정
    document.getElementById('user_title').innerText = data['user_nickname'];
    // 프로필 이미지 링크 설정
    document.getElementById('profilePic').src = data['user_profile_image_link']
    // 이름 GET
    document.getElementById('user_name').innerText = data['user_name'];
    // 닉네임 GET
    document.getElementById('usernickname').innerText = data['user_nickname'];
    // 자기소개 GET
    document.getElementById('user_profile').innerText = data['user_profile'];
    // 가입일자 GET
    document.getElementById('user_created_at').innerText = data['user_created_at'];
    // 유저 게시글 GET
    if( data['user_posting_data'].length != 0){
        document.getElementById('showpost_list_table').insertAdjacentHTML('beforeend', `
            <thead>
            <tr>
                <th>board_num</th>
                <th>title</th>
                <th>writer_nickname</th>
                <th>create_day</th>
                <th>tech_stack</th>
            </tr>
            </thead>
        `)
        for(i = 0; i < data['user_posting_data'].length; i++){
            const table = document.getElementById('user_posting_data_table')
            table.insertAdjacentHTML('beforeend', `
                <tr id="user_posting_data_table" onClick="location.href='/post/${data['user_posting_data'][i]['board_num']}'">
                    <td id="board_num">${data['user_posting_data'][i]['board_num']}</td>
                    <td id="board_title">${data['user_posting_data'][i]['title']}</td>
                    <td id="writer_nickname">${data['user_posting_data'][i]['writer_nickname']}</td>
                    <td id="create_day">${data['user_posting_data'][i]['create_day']}</td>
                    <td id="tech_stack">${data['user_posting_data'][i]['tech_stack']}</td>
                </tr>
            `)
        }
    }
}

// 페이지가 로드될 경우 GET 요청
window.onload = getUserData();


