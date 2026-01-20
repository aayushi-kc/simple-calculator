from flask import Flask, request

app = Flask(__name__)

# HTML template with embedded CSS and JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🧮 Simple Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 400px;
            margin: 50px auto;
            padding: 20px;
            text-align: center;
            background: #f5f5f5;
        }
        .calculator {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        input[type="number"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            font-size: 18px;
            border: 2px solid #ddd;
            border-radius: 5px;
        }
        select {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            font-size: 18px;
            border: 2px solid #ddd;
            border-radius: 5px;
        }
        button {
            width: 100%;
            padding: 15px;
            margin-top: 10px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 18px;
            cursor: pointer;
        }
        button:hover {
            background: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background: #e8f5e9;
            border-radius: 5px;
            font-size: 20px;
            font-weight: bold;
        }
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <h1>🧮 Simple Calculator</h1>

        <form method="POST" action="/calculate">
            <input type="number" step="any" name="num1" placeholder="Enter first number" required>

            <select name="operation" required>
                <option value="">Select Operation</option>
                <option value="add">➕ Addition (+)</option>
                <option value="subtract">➖ Subtraction (-)</option>
                <option value="multiply">✖️ Multiplication (*)</option>
                <option value="divide">➗ Division (/)</option>
            </select>

            <input type="number" step="any" name="num2" placeholder="Enter second number" required>

            <button type="submit">Calculate</button>
        </form>

        {% if result is not none %}
            <div class="result">
                {{ num1 }} {{ operator }} {{ num2 }} = {{ result }}
            </div>
        {% endif %}

        {% if error %}
            <div class="error">
                {{ error }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        return calculate()

    return HTML_TEMPLATE.replace('{% if result is not none %}', '')\
                       .replace('{% endif %}', '')\
                       .replace('{{ num1 }} {{ operator }} {{ num2 }} = {{ result }}', '')\
                       .replace('{% if error %}', '')\
                       .replace('{{ error }}', '')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get values from form
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operation = request.form['operation']

        # Perform calculation
        if operation == 'add':
            result = num1 + num2
            operator = '+'
        elif operation == 'subtract':
            result = num1 - num2
            operator = '-'
        elif operation == 'multiply':
            result = num1 * num2
            operator = '×'
        elif operation == 'divide':
            if num2 == 0:
                return HTML_TEMPLATE\
                    .replace('{% if result is not none %}', '')\
                    .replace('{% endif %}', '')\
                    .replace('{{ num1 }} {{ operator }} {{ num2 }} = {{ result }}', '')\
                    .replace('{% if error %}', 'error')\
                    .replace('{{ error }}', '❌ Cannot divide by zero!')
            result = num1 / num2
            operator = '÷'
        else:
            return HTML_TEMPLATE\
                .replace('{% if result is not none %}', '')\
                .replace('{% endif %}', '')\
                .replace('{{ num1 }} {{ operator }} {{ num2 }} = {{ result }}', '')\
                .replace('{% if error %}', 'error')\
                .replace('{{ error }}', '❌ Invalid operation!')

        # Render result
        return HTML_TEMPLATE\
            .replace('{% if result is not none %}', 'result')\
            .replace('{% endif %}', '')\
            .replace('{{ num1 }}', str(num1))\
            .replace('{{ operator }}', operator)\
            .replace('{{ num2 }}', str(num2))\
            .replace('{{ result }}', str(result))\
            .replace('{% if error %}', '')\
            .replace('{{ error }}', '')

    except ValueError:
        return HTML_TEMPLATE\
            .replace('{% if result is not none %}', '')\
            .replace('{% endif %}', '')\
            .replace('{{ num1 }} {{ operator }} {{ num2 }} = {{ result }}', '')\
            .replace('{% if error %}', 'error')\
            .replace('{{ error }}', '❌ Please enter valid numbers!')
    except Exception as e:
        return HTML_TEMPLATE\
            .replace('{% if result is not none %}', '')\
            .replace('{% endif %}', '')\
            .replace('{{ num1 }} {{ operator }} {{ num2 }} = {{ result }}', '')\
            .replace('{% if error %}', 'error')\
            .replace('{{ error }}', f'❌ Error: {str(e)}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)