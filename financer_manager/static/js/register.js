const username = document.querySelector('#usernameField')
const feedBack = document.querySelector('.invalid-feedback')
username.addEventListener('keyup', (e) => {
    console.log('77777', 77777)

    const usernameVal = e.target.value;

    username.classList.remove('is-invalid')
    feedBack.style.display='none'


    if(usernameVal.length > 0) {
        fetch('/auth/validate/', {
            body: JSON.stringify({ username: usernameVal }),
            method: 'POST',
        }).then(res=>res.json()).then(data => {
            console.log("data", data)
            if(data.username_error){
                username.classList.add('is-invalid')
                feedBack.style.display='block'
                feedBack.innerHTML = `<p>${data.username_error}</p>`
            }
        });
    }
})