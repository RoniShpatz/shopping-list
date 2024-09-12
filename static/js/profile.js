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

const requestFormPara = document.querySelector(".profile-request-div p");
const requestForm = document.querySelector(".profile-request-div");

if (!requestFormPara) {
    const newPara = document.createElement("p");
    newPara.innerHTML = '<span>No request to show.</span>';
    requestForm.appendChild(newPara);
}

const connectionFormPara = document.querySelector(".profile-connection-div p");
const connectionList = document.querySelector(".profile-connection-div li");

if (!connectionList && connectionFormPara) {
    connectionFormPara.innerText = "No connection yet";
}