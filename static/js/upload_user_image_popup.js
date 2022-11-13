import { getUserImage } from "./get_user_image.js"

const postUserImageSubmit = document.getElementById('openPopup_user_profile_image')
postUserImageSubmit.addEventListener('click', (e) => {
    var popup = window.open('/user/own_user/upload_image', 'window_name', 'width=430,height=500,location=no,status=no,scrollbars=no');
    popup.addEventListener('unload', function () {
        this.setTimeout(2000)
        getUserImage()
    });
})