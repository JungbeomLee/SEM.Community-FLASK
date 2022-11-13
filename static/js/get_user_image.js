function getUserImage() {
    fetch('/user/own_user/get', {
        method: 'GET'
    })
        .then(res => res.json())
        .then(data => {
            document.getElementById('profilePic').src = data['user_profile_image_link']
        })
}

export { getUserImage }