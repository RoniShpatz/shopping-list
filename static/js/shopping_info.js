const dateToHide = document.querySelectorAll(".date_to_hide")
const nameToHide = document.querySelectorAll(".name_to_hide")

dateToHide.forEach(input => {
    input.style.display = 'none'
})

nameToHide.forEach(input => {
    input.style.display = 'none'
})

const productName = document.querySelectorAll(".product_name")
const formAddProduct = document.querySelectorAll(".add_product_form")

let isOn = false
formAddProduct.forEach(form => {
    form.style.display = 'none'
})

productName.forEach((product,index) => {
    product.addEventListener("click", () => {
        if (isOn) {
            formAddProduct[index].style.display = 'inline'
            isOn = false
        } else {
            formAddProduct[index].style.display = 'none' 
            isOn = true
        } 
    })
})

