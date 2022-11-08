var popup;

function openPopup_have_profile_image() {
    popup = window.open('/user/own_user/upload_image', 'window_name', 'width=430,height=500,location=no,status=no,scrollbars=no');

    popup.addEventListener('unload', function () {
        var image = document.getElementById('profilePic')
        var temp = image.src
        var date = new Date()
        var cache_cracker = temp + "?" + date
        document.getElementById('profilePic').src = cache_cracker
    });
}

function openPopup_no_profile_image(user_link_primary) {
    popup = window.open('/user/own_user/upload_image', 'window_name', 'width=430,height=500,location=no,status=no,scrollbars=no'); 
    popup.addEventListener('unload', function () {
        var date = new Date()   
        var cache_cracker = "https://flask-user-image-storage.s3.ap-northeast-2.amazonaws.com/images/" + user_link_primary +".jpg?" + date
        this.setTimeout(3000)
        document.getElementById('profilePic').src = cache_cracker
    });
}