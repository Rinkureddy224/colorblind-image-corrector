document.addEventListener("DOMContentLoaded", function () {
    const surveyContainer = document.getElementById("survey-container");
    
    // Only run the survey logic if we're on the survey page
    if (!surveyContainer) {
        return; // Exit if not on the survey page
    }

    // 🚀 From here, place all your current script logic like before
    let userChoices = [];
    const colorList = ["red", "blue", "green", "yellow", "purple", "orange"];
    const questions = [
        { correctAnswer: "blue" },
        { correctAnswer: "green" },
        { correctAnswer: "yellow" },
        { correctAnswer: "purple" },
        { correctAnswer: "red" },
        { correctAnswer: "orange" }
    ];

    let currentQuestionIndex = 0;
    let totalQuestions = questions.length;

    // ... rest of your code (loadQuestion, handle clicks, etc.)
    function loadQuestion() {
        const question = questions[currentQuestionIndex];
        const questionContainer = document.getElementById('survey-container');
        const optionsContainer = document.querySelector('.options-container');

        document.getElementById('question-number').innerText = `Question ${currentQuestionIndex + 1}`;
        optionsContainer.innerHTML = '';
        const uniqueOptions = getUniqueOptions(colorList);
        shuffleArray(uniqueOptions);

        uniqueOptions.forEach(option => {
            const optionButton = document.createElement('button');
            optionButton.innerText = option;
            optionButton.classList.add('option-button');
            optionButton.onclick = () => handleOptionClick(option, question.correctAnswer);
            optionsContainer.appendChild(optionButton);
        });

        const colorBoxContainer = document.querySelector('.color-box-container');
        colorBoxContainer.innerHTML = '';
        const colorBox = document.createElement('div');
        colorBox.style.backgroundColor = question.correctAnswer;
        colorBox.classList.add('color-box');
        colorBoxContainer.appendChild(colorBox);
    }

    function getUniqueOptions(options) {
        return options.slice();
    }

    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    function handleOptionClick(option, correctAnswer) {
        userChoices.push({
            actualColor: correctAnswer,
            chosenColor: option
        });

        updateChoicesList();

        const buttons = document.querySelectorAll('.option-button');
        buttons.forEach(button => {
            if (button.innerText === option) {
                button.disabled = true;
            }
        });

        document.getElementById("next-button").style.display = "inline-block";

        if (userChoices.length === totalQuestions) {
            document.getElementById('survey-container').innerHTML = "<h2>Survey Complete! Now Click Continue to Upload Image!</h2>";
            document.getElementById("next-button").style.display = "none";
            document.getElementById("continue-button").style.display = "inline-block";
        }
    }

    function updateChoicesList() {
        const choicesList = document.getElementById('choices-list');
        choicesList.innerHTML = '';
        userChoices.forEach(choice => {
            const listItem = document.createElement('li');
            listItem.innerText = `Actual Color: ${choice.actualColor} - Chosen Color: ${choice.chosenColor}`;
            choicesList.appendChild(listItem);
        });
    }

    document.getElementById("next-button").addEventListener("click", function () {
        if (currentQuestionIndex < totalQuestions - 1) {
            currentQuestionIndex++;
            loadQuestion();
            this.style.display = "none";
        }
    });

    document.getElementById("continue-button").addEventListener("click", async function () {
        await submitSurveyData();
        localStorage.setItem("userChoices", JSON.stringify(userChoices));
        window.location.href = "/upload";
    });

    async function submitSurveyData() {
        const response = await fetch("/survey", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                responses: userChoices
            })
        });

        const data = await response.json();
        if (data.message) {
            console.log("Survey data sent successfully:", data.message);
        }
    }

    // Load the first question
    loadQuestion();
});
