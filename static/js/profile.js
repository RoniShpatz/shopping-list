const h2Username = document.querySelector(".username_on_off")
const changeNameForm = document.querySelector(".chage_name_form")
isClicked = false

 changeNameForm.style.display = 'none'

h2Username.addEventListener("click", () => {
    if (isClicked) {
        changeNameForm.style.display = 'none'
        isClicked = false
    } else {
        changeNameForm.style.display = 'inline'
        isClicked = true
    }
})

