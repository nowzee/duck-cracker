from datetime import datetime
import os
import time
from yaspin import yaspin

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
    <a href="{csv_file_name}" download>Download CSV</a>
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

graffiti = r"""
    .___             __                                         __                 
  __| _/_ __   ____ |  | __           ________________    ____ |  | __ ___________ 
 / __ |  |  \_/ ___\|  |/ /  ______ _/ ___\_  __ \__  \ _/ ___\|  |/ // __ \_  __ \
/ /_/ |  |  /\  \___|    <  /_____/ \  \___|  | \// __ \\  \___|    <\  ___/|  | \/
\____ |____/  \___  >__|_ \          \___  >__|  (____  /\___  >__|_ \\___  >__|   
     \/           \/     \/              \/           \/     \/     \/    \/       
    """


def rapports(results, algorithm, mode2, found_count, not_found_count, original_file, methode):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(graffiti)

    def generate_csv(results, file_name):
        with open(file_name, 'w', encoding='utf-8') as csv_file:
            csv_file.write("Hash,Word\n")
            for hashe, word in results.items():
                csv_file.write(f"{hashe},{word or 'not found'}\n")

    with yaspin(text="Making report file", color="magenta") as sp:
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

        os.makedirs(f"rapport/{current_time}")

        csv_file_name = f"rapport_{current_time}_.csv"
        generate_csv(results, os.path.join(f"rapport/{current_time}", csv_file_name))

        with open(os.path.join(f"rapport/{current_time}", f"rapport_{current_time}_.html"), "w", encoding="utf-8") as f:
            f.write(html_template.format(table_rows=table_rows, current_time=current_time, methode=methode,
                                         algorythm=algorithm, mode=mode2,
                                         Found=found_count, notfound=not_found_count, original_file=original_file,
                                         csv_file_name=csv_file_name))

        time.sleep(1)
        sp.write(f"✔ report file : rapport/{current_time}")

        # finalize
        sp.ok(f"✔")
