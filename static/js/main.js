const menu=document.querySelector(".menu")
const boton=document.querySelector(".boton")

boton.addEventListener("click", () => {
    if(menu.style.display == "block"){
        menu.style.display = "none"
    }else{
        menu.style.display = "block"
    }
    
})
