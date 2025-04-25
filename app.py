from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import os

app = Flask(__name__)
app.secret_key = 'guess-game-secret'  # Needed for session

# HTML + Tailwind (template string)
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Guess the Number</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen">
    <div class="bg-white p-10 rounded-lg shadow-md w-full max-w-md text-center">
        <h1 class="text-2xl font-bold mb-4">🎯 Guess the Number (1-100)</h1>
        {% if message %}
            <div class="mb-4 text-lg">{{ message }}</div>
        {% endif %}
        <form method="POST">
            <input type="number" name="guess" class="border p-2 rounded w-full mb-4" required min="1" max="100" placeholder="Enter your guess">
            <button class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded" type="submit">Guess</button>
        </form>
        {% if attempts > 0 %}
            <p class="mt-4 text-gray-600">Attempts: {{ attempts }}</p>
        {% endif %}
        {% if correct %}
            <a href="/" class="mt-4 inline-block text-blue-500 hover:underline">Play Again</a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def guess_game():
    if 'number' not in session:
        session['number'] = random.randint(1, 100)
        session['attempts'] = 0

    message = ''
    correct = False
    if request.method == 'POST':
        guess = int(request.form['guess'])
        session['attempts'] += 1
        if guess < session['number']:
            message = "Guess Higher 🔼"
        elif guess > session['number']:
            message = "Guess Lower 🔽"
        else:
            message = f"🎉 You guessed it right! The number was {session['number']}."
            message += f" It took you {session['attempts']} attempts."
            correct = True
            session.pop('number')
            session.pop('attempts')

    return render_template_string(html_template, message=message, attempts=session.get('attempts', 0), correct=correct)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use PORT provided by Render or default to 5000
    app.run(host='0.0.0.0', port=port)
