# Email Capture Quiz

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Discover Your Education Style</title>
<link rel="preconnect" href="[https://fonts.googleapis.com](https://fonts.googleapis.com/)">
<link rel="preconnect" href="[https://fonts.gstatic.com](https://fonts.gstatic.com/)" crossorigin>
<link href="[https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap](https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap)" rel="stylesheet">
<style>
* {
margin: 0;
padding: 0;
box-sizing: border-box;
}

```
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        line-height: 1.5;
        color: #2d3748;
        background: #f5f1ed;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
        -webkit-font-smoothing: antialiased;
    }

    .container {
        max-width: 600px;
        width: 100%;
        background: white;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        overflow: hidden;
    }

    .header {
        background: white;
        padding: 40px 30px 30px;
        text-align: center;
    }

    .header h1 {
        font-size: 2em;
        margin-bottom: 8px;
        font-weight: 700;
        color: #2d3748;
        line-height: 1.2;
    }

    .header .highlight {
        color: #f24915;
    }

    .header p {
        color: #718096;
        font-size: 1em;
        margin-bottom: 20px;
        font-weight: 400;
    }

    .progress {
        background: #e2e8f0;
        height: 2px;
        margin: 20px 0 0 0;
        overflow: hidden;
    }

    .progress-bar {
        background: #03a4ea;
        height: 100%;
        width: 0%;
        transition: width 0.3s ease;
    }

    .welcome-screen {
        padding: 40px 30px;
        text-align: center;
    }

    .welcome-screen h2 {
        font-size: 1.3em;
        margin-bottom: 12px;
        font-weight: 600;
        color: #2d3748;
        line-height: 1.4;
    }

    .welcome-screen p {
        color: #718096;
        font-size: 0.95em;
        margin-bottom: 28px;
        max-width: 460px;
        margin-left: auto;
        margin-right: auto;
    }

    .benefits {
        margin: 30px auto;
        text-align: left;
        max-width: 380px;
    }

    .benefit-item {
        display: flex;
        align-items: flex-start;
        margin-bottom: 12px;
        font-size: 0.95em;
        color: #2d3748;
    }

    .benefit-icon {
        width: 18px;
        height: 18px;
        flex-shrink: 0;
        margin-right: 12px;
        margin-top: 2px;
        color: #03a4ea;
        font-size: 16px;
        font-weight: 700;
    }

    .question-container {
        padding: 40px 30px;
        min-height: 350px;
        display: none;
    }

    .question-container.active {
        display: block;
    }

    .question h2 {
        font-size: 1.4em;
        margin-bottom: 24px;
        color: #2d3748;
        font-weight: 600;
        line-height: 1.4;
    }

    .options-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-bottom: 30px;
    }

    .option-btn {
        padding: 14px 18px;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        background: white;
        color: #2d3748;
        cursor: pointer;
        transition: all 0.15s ease;
        text-align: left;
        font-size: 15px;
        font-weight: 500;
        width: 100%;
    }

    .option-btn:hover {
        border-color: #03a4ea;
        background: #f7fafc;
    }

    .option-btn.selected {
        border-color: #03a4ea;
        background: #ebf8ff;
        color: #2d3748;
    }

    .button-container {
        display: flex;
        justify-content: center;
        gap: 10px;
    }

    .btn {
        padding: 12px 28px;
        border: none;
        border-radius: 6px;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        font-family: 'Inter', sans-serif;
    }

    .btn-primary {
        background: #f24915;
        color: white;
    }

    .btn-primary:hover:not(:disabled) {
        background: #d63f0f;
    }

    .btn-secondary {
        background: white;
        color: #4a5568;
        border: 1px solid #cbd5e0;
    }

    .btn-secondary:hover {
        background: #f7fafc;
    }

    .btn:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }

    .loading {
        text-align: center;
        padding: 60px 30px;
        display: none;
    }

    .loading .spinner {
        border: 2px solid #e2e8f0;
        border-top: 2px solid #03a4ea;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        animation: spin 0.8s linear infinite;
        margin: 0 auto 20px;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .email-capture {
        padding: 40px 30px;
        display: none;
        text-align: center;
    }

    .email-capture h2 {
        color: #2d3748;
        margin-bottom: 10px;
        font-size: 1.5em;
        font-weight: 600;
    }

    .email-capture p {
        color: #718096;
        margin-bottom: 24px;
        font-size: 0.95em;
    }

    .email-form {
        display: flex;
        flex-direction: column;
        gap: 12px;
        width: 100%;
        max-width: 320px;
        margin: 0 auto;
    }

    .email-input {
        padding: 12px 16px;
        border: 1px solid #cbd5e0;
        border-radius: 6px;
        font-size: 15px;
        font-family: 'Inter', sans-serif;
    }

    .email-input:focus {
        outline: none;
        border-color: #03a4ea;
    }

    .results {
        padding: 40px 30px;
        display: none;
    }

    .results h2 {
        color: #2d3748;
        margin-bottom: 24px;
        font-size: 1.6em;
        font-weight: 600;
        text-align: center;
    }

    .recommendation {
        background: #f7fafc;
        padding: 28px;
        border-radius: 8px;
        line-height: 1.6;
        font-size: 15px;
    }

    .philosophy-result {
        margin-bottom: 20px;
        padding: 16px;
        border-left: 3px solid #03a4ea;
        background: white;
        border-radius: 0 6px 6px 0;
    }

    .philosophy-result h3 {
        color: #2d3748;
        margin-bottom: 6px;
        font-weight: 600;
        font-size: 1.1em;
    }

    .percentage {
        font-weight: 700;
        color: #03a4ea;
    }

    .cta-buttons {
        text-align: center;
        margin-top: 28px;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
    }

    .cta-btn {
        background: #f24915;
        color: white;
        padding: 14px 24px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        font-size: 15px;
        min-width: 200px;
        display: inline-block;
        text-align: center;
        transition: all 0.2s ease;
    }

    .cta-btn:hover {
        background: #d63f0f;
    }

    .cta-btn.secondary {
        background: #03a4ea;
    }

    .cta-btn.secondary:hover {
        background: #0288c7;
    }

    @media (max-width: 600px) {
        .header {
            padding: 30px 20px 24px;
        }

        .header h1 {
            font-size: 1.6em;
        }

        .welcome-screen {
            padding: 30px 20px;
        }

        .question-container {
            padding: 30px 20px;
        }

        .cta-buttons {
            flex-direction: column;
        }

        .cta-btn {
            width: 100%;
            min-width: auto;
        }
    }
</style>

```

</head>
<body>
<div class="container">
<div class="header">
<h1>What's Your Homeschooling Style?</h1>
<div class="progress">
<div class="progress-bar" id="progressBar"></div>
</div>
</div>

```
    <div class="welcome-screen" id="welcomeScreen">
        <h2>What's Your Education Style?</h2>
        <p>Answer 5 simple questions to discover your approach and get personalized recommendations.</p>

        <div class="benefits">
            <div class="benefit-item">
                <div class="benefit-icon">✓</div>
                <span>Discover your top 3 education philosophies</span>
            </div>
            <div class="benefit-item">
                <div class="benefit-icon">✓</div>
                <span>Get personalized curriculum recommendations</span>
            </div>
            <div class="benefit-item">
                <div class="benefit-icon">✓</div>
                <span>Takes just 5 questions, under 3 minutes</span>
            </div>
        </div>

        <button class="btn btn-primary" id="startBtn">Start Assessment</button>
    </div>

    <div class="question-container" id="questionContainer">
        <div class="question">
            <h2 id="questionText">Loading...</h2>
            <div class="options-container" id="optionsContainer"></div>
            <div class="button-container">
                <button class="btn btn-secondary" id="backBtn" style="display: none;">Back</button>
                <button class="btn btn-primary" id="nextBtn" disabled>Next</button>
            </div>
        </div>
    </div>

    <div class="loading" id="loading">
        <div class="spinner"></div>
        <p style="color: #718096;">Analyzing your responses...</p>
    </div>

    <div class="email-capture" id="emailCapture">
        <h2>Get Your Results</h2>
        <p>Enter your email to receive your personalized profile.</p>
        <div class="email-form">
            <input type="email" id="emailInput" placeholder="your@email.com" class="email-input">
            <button class="btn btn-primary" id="submitEmailBtn">Email My Results</button>
            <button class="btn btn-secondary" id="skipEmailBtn">Skip for Now</button>
        </div>
    </div>

    <div class="results" id="results">
        <h2>Your Education Style</h2>
        <div class="recommendation" id="recommendationContent"></div>
    </div>
</div>

<script>
    const questionDatabase = {
        1: {
            id: 1,
            text: "What sounds most appealing to you?",
            options: [
                { text: "Following a proven, structured curriculum", value: "structured", next: "structured" },
                { text: "Letting curiosity guide learning", value: "child_led", next: "child_led" },
                { text: "Learning through projects and experiences", value: "project_based", next: "project_based" },
                { text: "Mixing approaches based on what works", value: "flexible", next: "flexible" }
            ]
        }
    };

    const philosophyDescriptions = {
        classical: { name: "Classical Education", description: "Time-tested approach with great books and formal logic", icon: "📚" },
        charlotte_mason: { name: "Charlotte Mason", description: "Living books, nature study, and short lessons", icon: "🌿" },
        montessori: { name: "Montessori", description: "Hands-on materials and self-directed learning", icon: "🔧" },
        unschooling: { name: "Unschooling", description: "Child-led learning through life experiences", icon: "🌱" }
    };

    let currentQuestionId = 0;
    let selectedAnswers = [];
    let philosophyScores = { classical: 0, charlotte_mason: 0, montessori: 0, unschooling: 0 };

    document.getElementById('startBtn').addEventListener('click', () => {
        document.getElementById('welcomeScreen').style.display = 'none';
        document.getElementById('questionContainer').classList.add('active');
        currentQuestionId = 1;
        loadQuestion(1);
    });

    function loadQuestion(questionId) {
        const question = questionDatabase[questionId];
        if (!question) return;

        document.getElementById('questionText').textContent = question.text;

        const optionsContainer = document.getElementById('optionsContainer');
        optionsContainer.innerHTML = '';

        question.options.forEach((option, index) => {
            const button = document.createElement('button');
            button.className = 'option-btn';
            button.textContent = option.text;
            button.onclick = () => selectOption(index, option);
            optionsContainer.appendChild(button);
        });

        document.getElementById('progressBar').style.width = (questionId / 5) * 100 + '%';
        document.getElementById('nextBtn').disabled = true;
    }

    function selectOption(index, option) {
        document.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('selected'));
        document.querySelectorAll('.option-btn')[index].classList.add('selected');
        selectedAnswers[currentQuestionId - 1] = option;
        document.getElementById('nextBtn').disabled = false;
    }

    document.getElementById('nextBtn').addEventListener('click', () => {
        document.getElementById('questionContainer').style.display = 'none';
        document.getElementById('loading').style.display = 'block';

        setTimeout(() => {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('emailCapture').style.display = 'block';
        }, 1200);
    });

    document.getElementById('skipEmailBtn').addEventListener('click', showResults);
    document.getElementById('submitEmailBtn').addEventListener('click', () => {
        console.log('Email:', document.getElementById('emailInput').value);
        showResults();
    });

    function showResults() {
        document.getElementById('emailCapture').style.display = 'none';

        let html = '<p style="margin-bottom: 24px; color: #4a5568;">Most families blend multiple approaches—this is open education.</p>';

        html += '<div class="cta-buttons">';
        html += '<a href="<https://opened.co>" target="_blank" class="cta-btn">Explore OpenEd Programs</a>';
        html += '<a href="<https://opened.co/tools>" target="_blank" class="cta-btn secondary">Browse Resources</a>';
        html += '</div>';

        document.getElementById('recommendationContent').innerHTML = html;
        document.getElementById('results').style.display = 'block';
    }
</script>

```

</body>
</html>