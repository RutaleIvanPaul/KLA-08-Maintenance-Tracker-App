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
	var signup_tab = document.getElementById("signup-tab");
	document.getElementById("login").style.display = "none";
	signup.style.display = "block";
	signup_tab.classList.add("active");
	document.getElementById("login-tab").classList.remove("active");

}

function displayFormLogin() {
	var login = document.getElementById("login");
	var login_tab = document.getElementById("login-tab");
	document.getElementById("signup").style.display = "none";
	login.style.display = "block";
	login_tab.classList.add("active");
	document.getElementById("signup-tab").classList.remove("active");

}

function redirectHome() {
	window.location.replace("homepage.html");
}

