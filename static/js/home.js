shoppingListName = document.querySelectorAll(".shopping_list_name_hidden");
shoppingListNameH2 = document.querySelectorAll(".list_name");
shoppingListOn = document.getElementById("hidden_shopping_list_name");
shoppingListEditForm = document.querySelectorAll(".shopping_list_name_edit_form")
let indexON = 0;  



window.addEventListener('load', (e) => {
    if (shoppingListOn) {
        shoppingListOn.style.display = 'none'
        shoppingListNameH2.forEach((h2, index) => {
            if (shoppingListOn.innerText === h2.innerText) {
                indexON = index; 
            }
        });
    }

  
    shoppingListNameH2.forEach((h2, index) => {
        shoppingListName[index].value = h2.innerText;

    });
    let etditShoppingListNameOn = false
    shoppingListEditForm.forEach(form => {
        form.style.display = "none"
    })
    shoppingListNameH2.forEach((h2, index) => {
        h2.addEventListener( "click", () => {
            if (etditShoppingListNameOn) {
                shoppingListEditForm[index].style.display = "none" 
                etditShoppingListNameOn = false
            } else {
                shoppingListEditForm[index].style.display = "inline"
                etditShoppingListNameOn = true
            }
        })
    })

    shoppingListInfoDiv.forEach((div, index) => {
        if (index === indexON) {
            div.style.display = "inline";
        } else {
            div.style.display = "none";
        }
    });
});


shoppingListName.forEach(input => {
    input.style.display = 'none';
});

shoppingListNameP = document.querySelectorAll(".shopping_list_name p");
shoppingListInfoDiv = document.querySelectorAll(".shopping_list_info");


shoppingListNameP.forEach((p, index) => {
    p.addEventListener("click", () => {
        shoppingListInfoDiv.forEach(div => {
            div.style.display = "none";
        });
        shoppingListInfoDiv[index].style.display = "inline";
        indexON = index; 
    });
});

itemId = document.querySelectorAll(".item_id_hidden")

itemId.forEach(item => {
    item.style.display = "none"
})

listItems = document.querySelectorAll(".list_item")
formEditItem = document.querySelectorAll(".edit_list_form")
isClicked = false

formEditItem.forEach(form => {
    form.style.display = "none"
})

listItems.forEach((item, index) => {
    item.addEventListener("click", () => {
        if (isClicked) {
        formEditItem[index].style.display = "inline"
        isClicked = false
        } else {
            formEditItem[index].style.display = "none"
            isClicked = true 
        }
    })
})

noProductsDiv = document.querySelectorAll(".no.products.yet")
if (noProductsDiv) {
    noProductsDiv.forEach(div =>{
        div.style.display = "none"
       
})
}



inputOldList = document.querySelectorAll(".edit_list_name_hidden")

inputOldList.forEach(input => {
    input.style.display = 'none'
})


flashMassage = document.querySelectorAll(".flash_massage")


