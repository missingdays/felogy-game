$.ajax({
  url: "/api/words",
  data: {
    fakeWords: 5,
    realWords: 5,
    language: 'english'
  },
  success: function( result ) {
  	$(".word").html(result["realWords"][0].word);
  	$(".definition").html(result["realWords"][0].definition);

  	console.log(result);
  }
});

$(".progress-bar").width("70%");
$(".progress-bar").html("7/10")