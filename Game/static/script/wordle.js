'use strict';


class Grid {
    constructor() {
    this.row = 1;
    this.col = 0;
    this.wordList = [];
    }

    addLetter(key) {
        if (this.col <5) {
            this.col++;

            grid.wordList.push(key)
            printToPage(key);
        }

    }

    removeLetter() {
        if (this.col > 0) {
            removeFromPage();
            this.col--;

            grid.wordList.pop()
        }
    }

    nextRow() {
        if (this.col === 5) {
            wordle.compare();
            wordle.winCheck();
            this.wordList = [];
            this.row++;
            this.col = 0;
        }
    }
    
    colorChange() {
        const element= document.getElementById(`${this.row}${wordle.colum+1}`);

        // Muuttaa taustavärin kirjaimille
        element.style.backgroundColor = wordle.letterColor;
    }


}


class Wordle {
    constructor(gridWeb, answer) {
        this.grid = gridWeb;
        this.letterColor = "#FFFFFF";
        this.progress = ["", "", "", "", ""];
        this.answer = answer
        this.colum = 0
    }

    compare() {
        const colors = ["#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF"];

        // Vihreät
        for (let i=0; i<5; i++) {
            if (this.grid.wordList[i] === this.answer[i]) {
                colors[i] = "#538D4E";

                this.progress[i] = grid.wordList[i];
            }
        }

        // Keltaiset
        for (let i=0; i<5; i++) {
            if (colors[i] === "#FFFFFF") {
                for (let k=0; k<5; k++) {
                    if (i !== k &&
                        this.grid.wordList[i] === this.answer[k] &&
                        this.grid.wordList[k] !== this.answer[k]) {
                        colors[i] = "#B59F3B";
                        break;
                    }
                }
            }
        }

        // Päivitä värit
        for (let i=0; i<5; i++) {
            this.letterColor = colors[i];
            this.colum = i;
            grid.colorChange();
        }

    }

    // kun voitto tapahtuu / häviö
    winCheck() {
        const element = document.querySelector('.winScreen')

        if (this.progress.join("") === this.answer.join("")) {
            alert("Voitit :) oikea sana on: " + wordle.answer)
            sendBoolean(true)
        } else if (grid.row > 5) {
            alert("Hävisit :( oikea sana oli: " + wordle.answer)
            sendBoolean(false)
        }
    }

}


function printToPage(key) {
    const row = grid.row;
    const col = grid.col;
    const p = document.createElement('p');
    const element= document.getElementById(`${row}${col}`);

    p.innerHTML = `${key}`;
    element.appendChild(p);
}

function removeFromPage() {
    const row = grid.row;
    const col = grid.col;
    const element= document.getElementById(`${row}${col}`);

    const child= element.firstElementChild
    element.removeChild(child);
}

function answerToList (answer = "KOIRA") {
    let answerListed = [];
    for (let i of answer) {
        answerListed.push(i);
    }
    return answerListed;
}

let grid;
let wordle;

// flask backend
document.addEventListener("DOMContentLoaded", async () => {
    fetch("/wordle/get_value")
        .then(res => res.json())
        .then(data => {
            const answer = data.value[0].toUpperCase();
            console.log(answer)
            grid = new Grid();
            wordle = new Wordle(grid, answerToList(answer))
        });

    await fetchStory()

    // 📌📌📌📌 STORY box sulkeminen 📌📌📌📌
    const storyContainer = document.getElementById('storyOverlay');
    const storyClose = document.getElementById('storyClose');
    storyClose.addEventListener('click', () => {
        storyContainer.className = 'story-hidden'
    })

});



document.addEventListener('keydown', (event) => {
    const key = event.key.toUpperCase();

    if (/^[A-ZÄÖÅ]$/i.test(key)) {
        grid.addLetter(key);
    }

    if (key === "ENTER") {
        grid.nextRow()
    }

    if (key === "BACKSPACE") {
        grid.removeLetter()
    }
});




//localStorage.setItem("sessionId", "moi");
//const sessionId = localStorage.getItem("sessionId")

