const form = document.getElementById('change_user_information');

form.addEventListener('submit', function (e) {
    e.preventDefault();

    const prePayload = new FormData(form);
    console.log(prePayload)
    const payload = new URLSearchParams(prePayload);

    fetch(location.href='/user/own_user/post', {
        method : 'POST',
        body : payload
    }) 
    .then(res => res.json())
    .then(data => console.log(data))
    .catch(err => console.log(err))


})