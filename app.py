import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Para não abrir janelas
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Cria a pasta de uploads se não existir
if not os.path.exists('uploads'):
    os.makedirs('uploads')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['csv_file']
    if file.filename == '':
        return redirect(url_for('index'))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    df = pd.read_csv(filepath)

    head = df.head().to_html(classes='table table-striped', index=False)
    tail = df.tail().to_html(classes='table table-striped', index=False)
    describe = df.describe().to_html(classes='table table-bordered')
    nulls = df.isnull().sum().to_frame(name="Missing Values").to_html(classes='table table-sm')

    # Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
    plt.tight_layout()
    heatmap_path = os.path.join('static', 'heatmap.png')
    plt.savefig(heatmap_path)
    plt.close()

    return render_template('result.html', head=head, tail=tail, describe=describe, nulls=nulls, heatmap_path=heatmap_path)


if __name__ == '__main__':
    app.run(debug=True)
