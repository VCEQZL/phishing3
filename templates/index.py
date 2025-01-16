<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Phishing URL Detection</title>
    <style>
        body {
            text-align: center;
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .container {
            margin-top: 50px;
        }
        h1 {
            color: #333;
        }
        .form-container {
            margin-top: 30px;
        }
        .form-container input[type="text"] {
            width: 300px;
            padding: 10px;
            margin-right: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .form-container button {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .form-container button:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 20px;
            font-size: 1.2em;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Phishing URL Detection</h1>
        <div class="form-container">
            <form method="POST">
                <input type="text" name="url" placeholder="Enter URL" required>
                <button type="submit">Check</button>
            </form>
        </div>
        {% if url %}
        <div class="result">
            <h2>URL: {{ url }}</h2>
            <h3>Result: {{ result }}</h3>
        </div>
        {% endif %}
    </div>
</body>
</html>
