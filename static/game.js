
const ADDITIONAL_WORDS_FACTOR = 5;

class Game {
    constructor(nWords, language){
        this.nWords = nWords;
        this.language = language;

        this.words = [];

        this.start();
    }

    loadWords(callback){
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

                if(callback){
                    callback();
                }
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
        const word = this.getCurrentWord();
        this.currentWord++;

        if(word.isFake == answer){
            this.score++;

            return true;
        }

        return false;

    }

    isOver(){
        return this.currentWord >= this.nWords;
    }

    getProgress(){
        return this.currentWord / this.nWords;
    }
}