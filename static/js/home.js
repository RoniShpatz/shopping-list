shoppingListName = document.querySelectorAll(".shopping_list_name_hidden")
shoppingListNameH2 = document.querySelectorAll(".list_name")


window.addEventListener('load', (e) => {
    shoppingListNameH2.forEach( (h2, index) => {
        shoppingListName[index].value =  h2.innerText 
    });
})


shoppingListName.forEach(input => {
input.style.display = 'none'
})

