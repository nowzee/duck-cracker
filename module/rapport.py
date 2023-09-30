from datetime import datetime
import os

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport</title>
    <style>
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }}
    </style>
</head>
<body>
    <h1>Rapport</h1>
    <h2>Generated at {current_time}</h2>

    <h3 style="margin: 0";>Method : {methode}</h3>
    <h3 style="margin: 0";>dictionary used : {original_file}</h3>
    <h3 style="margin: 0";>Mode : {mode}</h3>
    <h3 style="margin: 0";>Algorythm : {algorythm}</h3>
    <h3 style="margin: 1";>Found : {Found}&nbsp;&nbsp;Not Found : {notfound}</h3>
    <table>
        <thead>
            <tr>
                <th>Hash</th>
                <th>Word</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
</body>
</html>
"""


def rapports(results, algorithm, mode2, found_count, not_found_count, original_file, methode):
    table_rows = ''
    for hashe, word in results.items():
        word = word or 'not found'
        if word == 'not found':
            table_rows += f'<tr><td>{hashe}</td><td style="color:#FF0000";>{word}</td></tr>'
        else:
            table_rows += f"<tr><td>{hashe}</td><td>{word}</td></tr>"

    if not os.path.exists("rapport"):
        os.makedirs("rapport")

    now = datetime.now()
    current_time = now.strftime("%d_%H_%M_%S")
    with open(os.path.join("rapport", f"rapport_{current_time}_.html"), "w", encoding="utf-8") as f:
        f.write(html_template.format(table_rows=table_rows, current_time=current_time, methode=methode,
                                     algorythm=algorithm, mode=mode2,
                                     Found=found_count, notfound=not_found_count, original_file=original_file))
