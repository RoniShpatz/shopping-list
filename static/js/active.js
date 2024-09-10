const checkProductBtn = document.querySelectorAll(".check")
const missingProductBtn = document.querySelectorAll(".missing")

const productP = document.querySelectorAll(".product_p")

const hiddenCategory = document.querySelectorAll(".hidden-categorey")


const divMissing = document.getElementById("missing")
const divBought = document.getElementById("bought")

const hideProductId = document.querySelectorAll(".id_hidden")

const formSaveMissing = document.getElementById("form_save_missing")

hideProductId.forEach(span => {
    span.style.display = "none"
})

formSaveMissing.style.display = 'none';

hiddenCategory.forEach(category => {
    category.style.display = 'none'
})

checkProductBtn.forEach((check , index) => {
    check.addEventListener("click", () => {
        const parentDiv = productP[index].closest("div")
    
        productP[index].removeChild(checkProductBtn[index])
        productP[index].removeChild(missingProductBtn[index])
        divBought.appendChild(productP[index])
        hiddenCategory[index].style.display = 'inline'
        if (parentDiv.childElementCount <= 1) {
            parentDiv.style.display = 'none'
        }
    })
})

missingProductBtn.forEach((check , index) => {
    check.addEventListener("click", () => {
        const parentDiv = productP[index].closest("div")
    
        productP[index].removeChild(checkProductBtn[index])
        productP[index].removeChild(missingProductBtn[index])
        divMissing.appendChild(productP[index])
        hiddenCategory[index].style.display = 'inline'
        hiddenCategory[index].style.display = 'inline'
        if (parentDiv.childElementCount <= 1) {
            parentDiv.style.display = 'none'
        }
    })
})


// make the screen awake wile shopping

var wakeLock = null;
const canWakeLock = function(){
   return 'wakeLock' in navigator;
}
 
const setWakeLock = function () {
    if (!canWakeLock()) {
        console.error('Your browser is not support WakeLock API!');
        return;
    }
    if (wakeLock) {
        return;
    }
    navigator.wakeLock.request('screen').then(result => {
        wakeLock = result;
        console.log('Wake Lock is actived!');
        wakeLock.addEventListener('release', () => {
            wakeLock = null;
            console.log('Wake Lock is released!');
        });
    }).catch((err) => {
        console.error(`Wake Lock is faild：${err.message}`);
    });
};
 
setWakeLock();


// end shopping anf send info to backend

const endShopping = document.getElementById("end-shopping")

let missingList = []
let boughtList = []

// function that orginaize the data of the missing and bouht lists
function makeObject(listOfProducts) {
    return listOfProducts.map(item => {
        const [categoryPart, productInfoPart] = item.split(":");
        if (!productInfoPart) {
            console.error("Invalid format: ", item);
            return null;
        }
        
        const category = categoryPart.trim();
        const productInfo = productInfoPart.trim().split(/\s{2,}/);
        const [quantityName, productId] = productInfo;
        const [quantity, ...nameParts] = quantityName.trim().split(" "); 
        const name = nameParts.join(" ").trim();
        
        return {
            category: category,
            name: name,
            quantity: parseInt(quantity, 10),
            product_id: parseInt(productId.trim(), 10)
        };
    }).filter(obj => obj !== null); 
}

endShopping.addEventListener("click", () => {
    
    const missingData = divMissing.childNodes
    const boughtData = divBought.childNodes


  
    missingData.forEach(child => {
        if (child.tagName == "P") {
            const pText = child.textContent.trim();
            missingList .push(pText); 
        }
    })
    boughtData .forEach(child => {
        if (child.tagName == "P") {
            const pText = child.textContent.trim();
            boughtList.push(pText); 
        }
    })
    const missingObjects= makeObject(missingList)
    const boughtObjects = makeObject(boughtList)
    const dataToSend = {
        missingItems: missingObjects,
        boughtItems: boughtObjects
    };
    fetch('/end_shopping', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
    formSaveMissing.style.display = 'inline'
})









