
const ADDITIONAL_WORDS_FACTOR = 5;

class Game {
    constructor(nWords, language){
        this.nWords = nWords;
        this.language = language;

        this.words = [];

        this.start();
    }

    loadWords(){
        let totalWords = this.nWords * ADDITIONAL_WORDS_FACTOR;

        $.ajax({
            url: "/api/words",
            data: {
                fakeWords: totalWords,
                realWords: totalWords,
                language: this.language
            },
            success: result => {
                this.realWords = result.realWords;
                this.fakeWords = result.fakeWords;

                this.words = [];

                for(let i in this.realWords){
                    this.words.push({
                        word: this.realWords[i],
                        isFake: false
                    });
                }

                for(let i in this.fakeWords){
                    this.words.push({
                        word: this.fakeWords[i],
                        isFake: true
                    });
                }

                shuffle(this.words);
            }
        });
    }

    start(){
        this.currentWord = 0;
        this.score = 0;
    }

    getCurrentWord(){
        return this.words[this.currentWord];
    }

    makeMove(answer){
        if(this.getCurrentWord().isFake == answer){
            this.score++;
        }

        this.currentWord++;
    }

    isOver(){
        return this.currentWord == this.words.length;
    }
}