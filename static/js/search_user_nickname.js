window.addEventListener("keyup", (e) => {
    if(e.code === "Enter") {
        document.getElementById("search_button").click();
    }
})


const searchButton = document.getElementById('search_button')
searchButton.addEventListener('click', (e) => {
    function searchParam() {
        let searchValue = document.getElementById('search_user_name').value;
        if(searchValue != ''){
            location.href='/user/other_user?search='+searchValue
        }
    };

    searchParam()
})