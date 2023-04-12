const username = document.querySelector('#usernameField')
const feedBack = document.querySelector('.invalid-feedback')
const email = document.querySelector('#emailField')
const emailFeedBack = document.querySelector('.emailFeedBack')
const usernameSuccess = document.querySelector('.usernameSuccess')
const emailSuccess = document.querySelector('.emailSuccess')
const showPassword = document.querySelector('.showPassword')
const password = document.querySelector('#passwordField')
const submit = document.querySelector('.submit-btn')

const handleToggleInput = (e)=>{
    if(showPassword.textContent==='SHOW'){
        showPassword.textContent = 'HIDE';
        password.setAttribute("type","text")
    }else{
        showPassword.textContent = 'SHOW';
        password.setAttribute("type","password")
    }

}

showPassword.addEventListener('click', handleToggleInput)

email.addEventListener('keyup', (e) => {
    const emailVal = e.target.value;
    emailSuccess.style.display = 'block'
    emailSuccess.textContent = `Checking ${emailVal}`

    email.classList.remove('is-invalid')
    emailFeedBack.style.display='none'


    if(emailVal.length > 0) {
        fetch('/auth/validate-email/', {
            body: JSON.stringify({email: emailVal }),
            method: 'POST',
        }).then(res=>res.json()).then(data => {
            console.log("data", data)
            emailSuccess.style.display = 'none'
            if(data.email_error){
                submit.disabled = true
                email.classList.add('is-invalid')
                emailFeedBack.style.display='block'
                emailFeedBack.innerHTML = `<p>${data.email_error}</p>`
            }else{
                submit.removeAttribute('disabled')
            }
        });
    }
})

username.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;
    usernameSuccess.style.display = 'block'
    usernameSuccess.textContent = `Checking ${usernameVal}`

    username.classList.remove('is-invalid')
    feedBack.style.display='none'


    if(usernameVal.length > 0) {
        fetch('/auth/validate/', {
            body: JSON.stringify({ username: usernameVal }),
            method: 'POST',
        }).then(res=>res.json()).then(data => {
            console.log("data", data)
            usernameSuccess.style.display = 'none'
            if(data.username_error){
                username.classList.add('is-invalid')
                feedBack.style.display='block'
                feedBack.innerHTML = `<p>${data.username_error}</p>`
                submit.disabled = true
            }else{
                submit.removeAttribute('disabled')
            }
        });
    }
})