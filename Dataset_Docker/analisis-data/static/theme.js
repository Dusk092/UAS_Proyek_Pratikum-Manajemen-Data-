window.onload = function(){

    const tema =
    localStorage.getItem("theme")
    || "light";

    document.body.className =
    tema;

}