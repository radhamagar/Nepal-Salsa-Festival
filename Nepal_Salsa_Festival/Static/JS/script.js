const bars = document.querySelector(".bars");
const menu = document.querySelector(".container");
const close_btn = document.querySelector(".close-btn");

function toggleHide(item){
    if(item.classList.contains("hidden")){
        item.classList.remove("hidden");
    }else{
        item.classList.add("hidden");
    }

}

bars.addEventListener("click", ()=>{
    toggleHide(menu)
});

close_btn.addEventListener("click", ()=>{
    toggleHide(menu)   
});
