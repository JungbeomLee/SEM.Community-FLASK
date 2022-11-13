const passwordSubmit = document.getElementById('upload_user_image_button')
passwordSubmit.addEventListener('click', (e) => {
    function loadFetch() {
        e.preventDefault(); // 기본 폼 동작 막기
        let uploadUserImage = document.getElementById('upload_user_image').files[0];
        
        var formData = new FormData();
        formData.append('upload_user_image', uploadUserImage)
        console.log(formData)

        let check = {
            method: 'POST',
            body: formData,
            mode: 'no-cors'
        };

        postUserImage(check)
    };

    loadFetch()
})

function postUserImage(check) {
    fetch(`/user/own_user/upload_image/post`, check)
        .then(res => res.json())
        .then(data => {
            if(data['posting_image'] == true){
                document.getElementById('upload_user_image_form').style='display : none;'
                document.getElementById('image_upload_success').style ='display : block;'
            }else if(data['posting_image'] == false) {
                alert('Failed to upload image')
            }else{
                alert('ERROR')
            }
        })
}


