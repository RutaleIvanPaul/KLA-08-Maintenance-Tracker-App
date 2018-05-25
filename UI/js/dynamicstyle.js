function displayCommentBox() {
    var x = document.getElementById("commentbox");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function loadMenu(){
    var doc = document.querySelector('link[rel="import"]').import;
    var text = doc.querySelector('.menu');
    document.body.appendChild(text.cloneNode(true));
}
