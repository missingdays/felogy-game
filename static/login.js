
function registerUser(username, password, done, fail){
	$.post("/api/createUser", {
		"username": username,
		"password": password
	}).done(data => {
		done(data);
	}).fail(data => {
		fail(data);
	});
}

function handleLoginUser(){
	const username = $("#username").val();
	const password = $("#password").val();
	loginUser(username, password, data => {
	}, data => {
	});
}

function createAlert(options){
	const alert = $(`<div class="${options.classes}"> ${options.text} </div>`);

	setTimeout(function(){
		$(".alert").remove();
	}, 5000);

	return alert;
}

function handleRegisterUser(){
	const username = $("#username").val();
	const password = $("#password").val();
	registerUser(username, password, data => {
		$("body").append(createAlert({
			classes: "alert alert-success",
			text: "User was created successfully"
		}));
	}, data => {
		$("body").append(createAlert({
			classes: "alert alert-danger",
			text: "Some error occured"
		}));
	});
}