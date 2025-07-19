from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "API do TradeThomaz está no ar!"

# Necessário para rodar no Vercel
app.run()
Add api/index.py com código Flask
