let game;
let waitingForMove = true;

function startGame(language){
	game = new Game(10, language);

	game.loadWords(() => {
		updateViewBeforeMove();
	});
}

function updateViewBeforeMove(){

	if(game.isOver()){
		renderGameOver();
		return;
	}

	const word = game.getCurrentWord();

	$(".word").html(word.word.word);
	console.log(`${game.getProgress() * 100}%`);
	$(".progress-bar").width(`${game.getProgress() * 100}%`);
	$(".result").html("");

	$(".btn-fake").show();
	$(".btn-real").html("Real");

	$(".definition").html("");
}

function updateViewAfterMove(answer){
	const word = game.getCurrentWord();

	$(".definition").html(word.word.definition);
	$(".btn-fake").hide();
	$(".btn-real").html("Next");
	
	if(game.makeMove(answer)){
		$(".result").html("Correct");
	} else {
		$(".result").html("Wrong");
	}
}

function makeMove(answer){
	if(waitingForMove){

		if(game.isOver()){
			return;
		}

		updateViewAfterMove(answer);
		waitingForMove = false;
	} else {
		updateViewBeforeMove();
		waitingForMove = true;
	}
}

function renderGameOver(){
	const gameContainer = $(".game");
	gameContainer.html(
		`<div class="jumbotron">
			<h1 class="display-4"> Score: ${game.score} / ${game.nWords} </h1>
			<a class="btn btn-primary btn-lg" href="/" role="button">To main menu</a>
			<a class="btn btn-primary btn-lg" href="/game.html" role="button">New game</a>
		</div>`)
}

function fakeClicked(){
	makeMove(true);
}

function realClicked(){
	makeMove(false);
}

$(document).keypress(event => {
	const char = String.fromCharCode(event.which);

	if(char == 'f'){
		fakeClicked();
	} else if(char == 'j'){
		realClicked();
	}
});

startGame(getUrlParameter("language"));