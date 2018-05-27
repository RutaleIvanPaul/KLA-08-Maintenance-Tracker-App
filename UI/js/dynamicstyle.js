function displayCommentBox() {
    var x = document.getElementById("commentbox");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function loadMenu() {
    var doc = document.querySelector('link[rel="import"]').import;
    var text = doc.querySelector('.menu');
    document.body.appendChild(text.cloneNode(true));
}

function displayFormSignup() {
    var signup = document.getElementById("signup");
    document.getElementById("login").style.display = "none";
    signup.style.display = "block";

}

function displayFormLogin() {
    var login = document.getElementById("login");
    document.getElementById("signup").style.display = "none";
    login.style.display = "block";

}

function redirectHome(){
    window.location.replace("homepage.html");
}

