from flask import Flask, request, render_template_string
import math

app = Flask(__name__)

# HTML template with embedded CSS and JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🧮 Advanced Calculator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: flex-start;
        }

        .calculator-container {
            max-width: 1000px;
            width: 100%;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .header h1 {
            font-size: clamp(1.8rem, 4vw, 2.5rem);
            margin-bottom: 10px;
        }

        .header p {
            font-size: clamp(1rem, 2vw, 1.2rem);
            opacity: 0.9;
        }

        .calculator-tabs {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            margin-bottom: 25px;
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }

        .tab-btn {
            background: rgba(255,255,255,0.9);
            border: none;
            padding: clamp(12px, 2vw, 15px) clamp(20px, 3vw, 30px);
            border-radius: 50px;
            font-size: clamp(14px, 2vw, 16px);
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #333;
            flex: 1;
            min-width: 120px;
            max-width: 200px;
        }

        .tab-btn:hover {
            background: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        .tab-btn.active {
            background: #4CAF50;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(76,175,80,0.3);
        }

        .calculator-box {
            background: white;
            border-radius: 20px;
            padding: clamp(20px, 4vw, 40px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }

        .calculator-form {
            display: none;
            animation: fadeIn 0.5s ease;
        }

        .calculator-form.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .form-group {
            margin-bottom: 25px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
            font-size: clamp(14px, 2vw, 16px);
        }

        .form-group input[type="number"],
        .form-group select {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
            background: #f9f9f9;
        }

        .form-group input[type="number"]:focus,
        .form-group select:focus {
            outline: none;
            border-color: #4CAF50;
            background: white;
        }

        .form-row {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 15px;
        }

        .form-col {
            flex: 1;
            min-width: 200px;
        }

        .calculate-btn {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            border: none;
            padding: 18px 30px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
            margin-top: 20px;
            box-shadow: 0 5px 15px rgba(76,175,80,0.3);
        }

        .calculate-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(76,175,80,0.4);
        }

        .calculate-btn:active {
            transform: translateY(-1px);
        }

        .result-container {
            margin-top: 30px;
            padding: 25px;
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            border-radius: 15px;
            border-left: 5px solid #4CAF50;
            display: none;
            animation: slideIn 0.5s ease;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .result-container.show {
            display: block;
        }

        .result-title {
            color: #2e7d32;
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .result-title i {
            font-size: 24px;
        }

        .result-content {
            font-size: 18px;
            line-height: 1.6;
            color: #333;
        }

        .error-message {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            border-left: 5px solid #c62828;
            display: none;
            animation: shake 0.5s ease;
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }

        .error-message.show {
            display: block;
        }

        .footer {
            text-align: center;
            color: white;
            margin-top: 30px;
            padding: 20px;
            font-size: 14px;
            opacity: 0.8;
        }

        /* Mobile-specific styles */
        @media (max-width: 768px) {
            body {
                padding: 15px;
                align-items: flex-start;
            }

            .calculator-box {
                padding: 20px;
                border-radius: 15px;
            }

            .tab-btn {
                padding: 12px 15px;
                font-size: 14px;
                min-width: 100px;
            }

            .form-group input[type="number"],
            .form-group select {
                padding: 12px;
                font-size: 15px;
            }

            .calculate-btn {
                padding: 15px;
                font-size: 16px;
            }

            .result-container {
                padding: 20px;
            }

            .result-content {
                font-size: 16px;
            }
        }

        @media (max-width: 480px) {
            .calculator-tabs {
                flex-direction: column;
                align-items: center;
            }

            .tab-btn {
                width: 100%;
                max-width: 100%;
            }

            .form-row {
                flex-direction: column;
                gap: 10px;
            }

            .form-col {
                min-width: 100%;
            }
        }

        /* Touch device optimizations */
        @media (hover: none) {
            .tab-btn:hover,
            .calculate-btn:hover {
                transform: none;
            }

            .tab-btn:active,
            .calculate-btn:active {
                transform: scale(0.98);
            }
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <div class="calculator-container">
        <div class="header">
            <h1><i class="fas fa-calculator"></i> Advanced Calculator</h1>
            <p>Choose from Basic, SI (Simple Interest), or EMI Calculator</p>
        </div>

        <div class="calculator-tabs">
            <button class="tab-btn active" onclick="showTab('basic')">
                <i class="fas fa-calculator"></i> Basic Calculator
            </button>
            <button class="tab-btn" onclick="showTab('si')">
                <i class="fas fa-percentage"></i> SI Calculator
            </button>
            <button class="tab-btn" onclick="showTab('emi')">
                <i class="fas fa-home"></i> EMI Calculator
            </button>
        </div>

        <!-- Basic Calculator Form -->
        <div class="calculator-box">
            <form id="basicForm" class="calculator-form active" method="POST" action="/calculate/basic">
                <div class="form-group">
                    <label for="num1"><i class="fas fa-hashtag"></i> First Number</label>
                    <input type="number" step="any" id="num1" name="num1" placeholder="Enter first number" required>
                </div>

                <div class="form-group">
                    <label for="operation"><i class="fas fa-cogs"></i> Operation</label>
                    <select id="operation" name="operation" required>
                        <option value="">Select Operation</option>
                        <option value="add">➕ Addition (+)</option>
                        <option value="subtract">➖ Subtraction (-)</option>
                        <option value="multiply">✖️ Multiplication (×)</option>
                        <option value="divide">➗ Division (÷)</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="num2"><i class="fas fa-hashtag"></i> Second Number</label>
                    <input type="number" step="any" id="num2" name="num2" placeholder="Enter second number" required>
                </div>

                <button type="submit" class="calculate-btn">
                    <i class="fas fa-calculator"></i> Calculate
                </button>
            </form>

            <!-- SI Calculator Form -->
            <form id="siForm" class="calculator-form" method="POST" action="/calculate/si">
                <div class="form-row">
                    <div class="form-col">
                        <div class="form-group">
                            <label for="principal"><i class="fas fa-money-bill-wave"></i> Principal Amount (Rs)</label>
                            <input type="number" step="any" id="principal" name="principal" placeholder="Enter principal" required min="0">
                        </div>
                    </div>

                    <div class="form-col">
                        <div class="form-group">
                            <label for="rate"><i class="fas fa-percentage"></i> Interest Rate (% per year)</label>
                            <input type="number" step="0.01" id="rate" name="rate" placeholder="Enter rate" required min="0" max="100">
                        </div>
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-col">
                        <div class="form-group">
                            <label for="time"><i class="fas fa-clock"></i> Time Period (years)</label>
                            <input type="number" step="any" id="time" name="time" placeholder="Enter time" required min="0">
                        </div>
                    </div>

                    <div class="form-col">
                        <div class="form-group">
                            <label for="si_type"><i class="fas fa-calendar-alt"></i> Interest Type</label>
                            <select id="si_type" name="si_type">
                                <option value="years">Years</option>
                                <option value="months">Months</option>
                                <option value="days">Days</option>
                            </select>
                        </div>
                    </div>
                </div>

                <button type="submit" class="calculate-btn">
                    <i class="fas fa-calculator"></i> Calculate SI
                </button>
            </form>

            <!-- EMI Calculator Form -->
            <form id="emiForm" class="calculator-form" method="POST" action="/calculate/emi">
                <div class="form-row">
                    <div class="form-col">
                        <div class="form-group">
                            <label for="loan_amount"><i class="fas fa-home"></i> Loan Amount (Rs)</label>
                            <input type="number" step="any" id="loan_amount" name="loan_amount" placeholder="Enter loan amount" required min="0">
                        </div>
                    </div>

                    <div class="form-col">
                        <div class="form-group">
                            <label for="interest_rate"><i class="fas fa-percentage"></i> Annual Interest Rate (%)</label>
                            <input type="number" step="0.01" id="interest_rate" name="interest_rate" placeholder="Enter interest rate" required min="0" max="100">
                        </div>
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-col">
                        <div class="form-group">
                            <label for="loan_tenure"><i class="fas fa-calendar"></i> Loan Tenure</label>
                            <input type="number" step="any" id="loan_tenure" name="loan_tenure" placeholder="Enter tenure" required min="0">
                        </div>
                    </div>

                    <div class="form-col">
                        <div class="form-group">
                            <label for="tenure_type"><i class="fas fa-clock"></i> Tenure Type</label>
                            <select id="tenure_type" name="tenure_type">
                                <option value="years">Years</option>
                                <option value="months">Months</option>
                            </select>
                        </div>
                    </div>
                </div>

                <button type="submit" class="calculate-btn">
                    <i class="fas fa-calculator"></i> Calculate EMI
                </button>
            </form>

            <!-- Results Container -->
            <div id="resultContainer" class="result-container"></div>

            <!-- Error Container -->
            <div id="errorContainer" class="error-message"></div>
        </div>

        <div class="footer">
            <p>Advanced Calculator | Made with Flask | Responsive Design for PC & Mobile</p>
        </div>
    </div>

    <script>
        // Tab switching functionality
        function showTab(tabName) {
            // Hide all forms
            document.querySelectorAll('.calculator-form').forEach(form => {
                form.classList.remove('active');
            });

            // Remove active class from all buttons
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });

            // Show selected form and activate button
            document.getElementById(tabName + 'Form').classList.add('active');
            event.target.classList.add('active');

            // Clear previous results
            document.getElementById('resultContainer').classList.remove('show');
            document.getElementById('errorContainer').classList.remove('show');
        }

        // Form submission with AJAX
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', async function(e) {
                e.preventDefault();

                // Clear previous results
                document.getElementById('resultContainer').classList.remove('show');
                document.getElementById('errorContainer').classList.remove('show');

                // Show loading state
                const submitBtn = this.querySelector('.calculate-btn');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Calculating...';
                submitBtn.disabled = true;

                try {
                    const formData = new FormData(this);
                    const response = await fetch(this.action, {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();

                    if (data.success) {
                        // Display result
                        const resultContainer = document.getElementById('resultContainer');
                        resultContainer.innerHTML = `
                            <div class="result-title">
                                <i class="fas fa-check-circle"></i> ${data.title}
                            </div>
                            <div class="result-content">
                                ${data.result_html}
                            </div>
                            ${data.details ? `<div class="result-details" style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #ccc;">
                                ${data.details}
                            </div>` : ''}
                        `;
                        resultContainer.classList.add('show');

                        // Scroll to result
                        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    } else {
                        // Display error
                        const errorContainer = document.getElementById('errorContainer');
                        errorContainer.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${data.error}`;
                        errorContainer.classList.add('show');

                        // Scroll to error
                        errorContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    }
                } catch (error) {
                    // Display network error
                    const errorContainer = document.getElementById('errorContainer');
                    errorContainer.innerHTML = `<i class="fas fa-exclamation-triangle"></i> Network error. Please try again.`;
                    errorContainer.classList.add('show');

                    // Scroll to error
                    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                } finally {
                    // Restore button
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
            });
        });

        // Auto-focus first input in active form
        function focusFirstInput() {
            const activeForm = document.querySelector('.calculator-form.active');
            if (activeForm) {
                const firstInput = activeForm.querySelector('input, select');
                if (firstInput) firstInput.focus();
            }
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', focusFirstInput);

        // Add keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                const activeForm = document.querySelector('.calculator-form.active');
                if (activeForm) {
                    activeForm.querySelector('.calculate-btn').click();
                }
            }

            // Tab switching with arrow keys
            if (e.altKey && e.key >= '1' && e.key <= '3') {
                const tabs = ['basic', 'si', 'emi'];
                const tabIndex = parseInt(e.key) - 1;
                if (tabs[tabIndex]) {
                    showTab(tabs[tabIndex]);
                }
            }
        });

        // Mobile touch improvements
        document.querySelectorAll('input, select').forEach(input => {
            input.addEventListener('touchstart', function() {
                this.style.transform = 'scale(0.98)';
            });

            input.addEventListener('touchend', function() {
                this.style.transform = 'scale(1)';
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_TEMPLATE

@app.route('/calculate/basic', methods=['POST'])
def calculate_basic():
    try:
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operation = request.form['operation']

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
                return {
                    'success': False,
                    'error': '❌ Cannot divide by zero!'
                }
            result = num1 / num2
            operator = '÷'
        else:
            return {
                'success': False,
                'error': '❌ Invalid operation selected!'
            }

        return {
            'success': True,
            'title': 'Basic Calculation Result',
            'result_html': f'''
                <div style="font-size: 1.2em; margin-bottom: 10px;">
                    <strong>{num1} {operator} {num2} = {result:.6f}</strong>
                </div>
                <div style="color: #666; font-size: 0.9em;">
                    Result: <strong>{result:,.6f}</strong>
                </div>
            '''
        }

    except ValueError:
        return {
            'success': False,
            'error': '❌ Please enter valid numbers!'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'❌ Error: {str(e)}'
        }

@app.route('/calculate/si', methods=['POST'])
def calculate_si():
    try:
        principal = float(request.form['principal'])
        rate = float(request.form['rate'])
        time = float(request.form['time'])
        si_type = request.form.get('si_type', 'years')

        if principal <= 0 or rate <= 0 or time <= 0:
            return {
                'success': False,
                'error': '❌ All values must be positive numbers!'
            }

        # Convert time to years based on type
        if si_type == 'months':
            time_years = time / 12
        elif si_type == 'days':
            time_years = time / 365
        else:
            time_years = time

        # Calculate Simple Interest
        interest = (principal * rate * time_years) / 100
        total_amount = principal + interest

        return {
            'success': True,
            'title': 'Simple Interest Calculation',
            'result_html': f'''
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 10px;">
                    <div style="background: #4CAF50; color: white; padding: 15px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 0.9em; opacity: 0.9;">Principal</div>
                        <div style="font-size: 1.5em; font-weight: bold;">₹{principal:,.2f}</div>
                    </div>
                    <div style="background: #2196F3; color: white; padding: 15px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 0.9em; opacity: 0.9;">Interest</div>
                        <div style="font-size: 1.5em; font-weight: bold;">₹{interest:,.2f}</div>
                    </div>
                    <div style="background: #FF9800; color: white; padding: 15px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 0.9em; opacity: 0.9;">Total Amount</div>
                        <div style="font-size: 1.5em; font-weight: bold;">₹{total_amount:,.2f}</div>
                    </div>
                </div>
            ''',
            'details': f'''
                <div style="color: #666; font-size: 0.9em;">
                    <strong>Calculation Details:</strong><br>
                    • Principal: Rs{principal:,.2f}<br>
                    • Rate: {rate}% per year<br>
                    • Time: {time} {si_type}<br>
                    • Simple Interest: Rs{interest:,.2f}<br>
                    • Total Amount: Rs{total_amount:,.2f}
                </div>
            '''
        }

    except ValueError:
        return {
            'success': False,
            'error': '❌ Please enter valid numbers!'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'❌ Error: {str(e)}'
        }

@app.route('/calculate/emi', methods=['POST'])
def calculate_emi():
    try:
        loan_amount = float(request.form['loan_amount'])
        interest_rate = float(request.form['interest_rate'])
        loan_tenure = float(request.form['loan_tenure'])
        tenure_type = request.form.get('tenure_type', 'years')

        if loan_amount <= 0 or interest_rate <= 0 or loan_tenure <= 0:
            return {
                'success': False,
                'error': '❌ All values must be positive numbers!'
            }

        # Convert tenure to months
        if tenure_type == 'years':
            tenure_months = loan_tenure * 12
        else:
            tenure_months = loan_tenure

        # Calculate EMI
        monthly_rate = interest_rate / 12 / 100
        emi = loan_amount * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)

        # Calculate total payment and interest
        total_payment = emi * tenure_months
        total_interest = total_payment - loan_amount

        return {
            'success': True,
            'title': 'EMI Calculation Result',
            'result_html': f'''
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 10px;">
                    <div style="background: #9C27B0; color: white; padding: 15px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 0.9em; opacity: 0.9;">Monthly EMI</div>
                        <div style="font-size: 1.5em; font-weight: bold;">₹{emi:,.2f}</div>
                    </div>
                    <div style="background: #FF5722; color: white; padding: 15px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 0.9em; opacity: 0.9;">Total Interest</div>
                        <div style="font-size: 1.5em; font-weight: bold;">₹{total_interest:,.2f}</div>
                    </div>
                    <div style="background: #009688; color: white; padding: 15px; border-radius: 10px; text-align: center;">
                        <div style="font-size: 0.9em; opacity: 0.9;">Total Payment</div>
                        <div style="font-size: 1.5em; font-weight: bold;">₹{total_payment:,.2f}</div>
                    </div>
                </div>
            ''',
            'details': f'''
                <div style="color: #666; font-size: 0.9em;">
                    <strong>Loan Breakdown:</strong><br>
                    • Loan Amount: Rs{loan_amount:,.2f}<br>
                    • Annual Interest Rate: {interest_rate}%<br>
                    • Loan Tenure: {loan_tenure} {tenure_type} ({tenure_months} months)<br>
                    • Monthly EMI: Rs{emi:,.2f}<br>
                    • Total Interest Payable: Rs{total_interest:,.2f}<br>
                    • Total Payment: Rs{total_payment:,.2f}
                </div>
            '''
        }

    except ValueError:
        return {
            'success': False,
            'error': '❌ Please enter valid numbers!'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'❌ Error: {str(e)}'
        }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)