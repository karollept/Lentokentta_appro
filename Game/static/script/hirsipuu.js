'use strict'

class hirsiPuu {
    constructor(answer, answerMystery) {
    this.answer = answer;
    this.progress = answerMystery;
    this.update = false;
    this.picture = 0;
    this.guessedWord = "";
    this.win = null;
    this.hangmanPictures =[
        "../images/hirsipuu2.png",
        "../images/hirsipuu3.png",
        "../images/hirsipuu4.png",
        "../images/hirsipuu5.png",
        "../images/hirsipuu6.png",
        "../images/hirsipuu7.png",
        "../images/hirsipuu8.png",
        "../images/hirsipuu9.png"
        ];
    }

    wordGuess (guess) {
        this.guessedWord = guess

    }

    letterGuess (letter) {
        /*Jos kirjain oikea päivittää progress listan jos ei, niin update = true*/
        for (let i = 0; i < this.answer.length; i++) {
            if (letter === this.answer[i] && this.progress[i] === "_") {
                this.progress[i] = letter;
                this.update = true;
            }
        }
    }

    addGuess (letter) {
        const element = document.querySelector('#guessed');
        let innerHTML = element.innerHTML;
        innerHTML += (" " + letter);

        element.innerHTML = innerHTML;
    }

    updateProgress () {
        const element = document.querySelector(".correctLetters");
        let print ="";
        for (let i of this.progress) {
            print += i +" ";
        }
        element.innerHTML = print;
    }

    updatePicture () {
        const element = document.querySelector('#hangman-img')
        if (this.update === false) {
            element.src= this.hangmanPictures[this.picture]
            this.picture ++;
        } else {this.update = false;}

    }

    winCheck() {
        // kirjainten onnistunut arvaus
        if (this.progress.join("") === this.answer.join("")) {
            this.win = true;
            return;
        }

        // sanan arvaus (guessedWord on string, ei array)
        if (this.guessedWord === this.answer.join("")) {
            this.progress = this.answer.slice(); // päivitetään progress näyttämään sana
            this.win = true;
        }
    }
    loseCheck() {
    // Jos kuvaindeksi ylittää viimeisen kuvan
        if (this.picture >= this.hangmanPictures.length) {
            this.win = false;
            return true;
        }
        return false;
}

}

function stringToArray (string) {
    let array = [];
    for (let i of string) {
        array.push(i);
    }
    return array;
}

let answer;
let printToPage = [];
let hp;
document.addEventListener("DOMContentLoaded", async () => {
    const timestamp = new Date().getTime();
    fetch("/hirsipuu/get_value")
        .then(res => res.json())
        .then(data => {

            answer = stringToArray(data.value[0].toUpperCase());
            for (let i = 0; i < answer.length; i++) {
            printToPage.push("_");
            }
            hp = new hirsiPuu(answer, printToPage);
            hp.updateProgress();
            console.log(data.value[0])
        });

    fetch("/info")
        .then(response => response.json())
        .then(data => {
            const location = data.location;
            const budget = data.budget;

            const elementBudget = document.getElementById('budget');
            const elementLocation = document.getElementById('location');

            elementBudget.innerHTML = budget + "€";
            elementLocation.innerHTML = location;
        })

    await fetchStory()
    // 📌📌📌📌 STORY box sulkeminen 📌📌📌📌
    const storyContainer = document.getElementById('storyOverlay');
    const storyClose = document.getElementById('storyClose');
    storyClose.addEventListener('click', () => {
        storyContainer.className = 'story-hidden'
    })

});




const guessButton = document.querySelector('#guessButton')
guessButton.addEventListener('click', (e) => {
    e.preventDefault();
    const guessInput = document.querySelector('#guessInput');
    const guessValue = guessInput.value.toUpperCase();
    guessInput.value = "";

    // yksi kirjain
    if (/^[A-ZÖÄÅ]$/.test(guessValue)) {

        hp.letterGuess(guessValue);
        hp.addGuess(guessValue);

    } else {
        // sanan arvaus
        let cleanWord = "";

        for (let i of guessValue) {
            if (/^[A-ZÖÄÅ]$/.test(i)) cleanWord += i;
        }

        hp.wordGuess(cleanWord);
    }

    hp.winCheck();

    if (hp.win !== true) {
        hp.updatePicture();
    }

    if (hp.loseCheck()) {
        alert(`Hävisit, oikea sana oli: ${answer.join("")}`);
        sendBoolean(false)
        return;
    }

    hp.updateProgress();

    if (hp.win === true) {
        alert("Voitit!");
        sendBoolean(true)
    }

});
