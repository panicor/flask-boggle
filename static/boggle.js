class Game{
    constructor(id, seconds = 60){
        this.seconds = seconds
        this.displayTimer()

        this.words = new Set();
        this.board = $("#" + id)
        this.score = 0

        this.timer = setInterval(this.passSeconds.bind(this), 1000)
        
        $(".word-form", this.board).on("submit", this.makeSubmit.bind(this));
    }

    displayWord(word){
        $(".words", this.board).append($("<li>", { text: word}))
    }

    displayMsg(message, cls){
        $(".msg", this.board).text(message).removeClass().addClass(`msg ${cls}`)
    }

    displayScore(){
        $(".score", this.board).text(this.score)
    }

    displayTimer(){
        $(".timer", this.board).text(this.seconds)
    }

    async makeSubmit(e){
        e.preventDefault();
        const $word = $(".word", this.board)
        let word = $word.val()

        if(!word){
            return;
        }

        if(this.words.has(word)){
            this.displayMsg(`${word} already found`);
            return
        }

        let resp = await axios.get("/check", { params: { word: word }}) 
        console.log(resp.data);

        console.log("WORD:" + word)
        if(resp.data.res === "not-word"){
            this.displayMsg(`${word} is not a word`)
        }
        else if(resp.data.res === "not-on-board"){
            this.displayMsg(`${word} is not on board`)
        }
        else{
            this.displayWord(word)
            this.score += word.length
            this.displayScore()
            this.words.add(word)
            this.displayMsg(`${word} added`)
        }

        $word.val("") 
}

    async passSeconds(){
        this.seconds-=1
        this.displayTimer()

        if(this.seconds === 0){
            clearInterval(this.timer)
            await this.scoreBoggle()
        }
    }


    async scoreBoggle(){
        $(".word-form", this.board).hide()

        let resp = await axios.post("/final-score", {score: this.score})

        console.log(resp.data)

        if(resp.data.record){
            this.displayMsg(`New Record: ${this.score}`, "ok")
        }
        else{
            this.displayMsg(`Game over`, "ok")
        }
    }
}