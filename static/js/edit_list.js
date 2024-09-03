noProductsDiv = document.querySelectorAll(".no.products.yet")
if (noProductsDiv) {
    noProductsDiv.forEach(div =>{
        div.style.display = "none"
       
})
}

const inputProductIdHidden = document.querySelectorAll(".product_id_hidden")

inputProductIdHidden.forEach(input => {
    input.style.display = "none"
})

let isClicked = false

const formApearOnclick = document.querySelectorAll(".edit_list_form_onclick")
const praraProductItem = document.querySelectorAll(".edit_product_item")

formApearOnclick.forEach(form => {
    form.style.display = 'none'
})

praraProductItem.forEach((para, index) => {
    para.addEventListener("click", () => {
        if (isClicked) {
            formApearOnclick[index].style.display = 'inline'
            isClicked = false
        } else {
            formApearOnclick[index].style.display = 'none'
            isClicked = true
        }
    })
})

