from flask import Flask, render_template, redirect, url_for
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)

produtos = [
    {"id": 1, "nome": "Notebook", "preco": 3500.00, "status": "PENDENTE"},
    {"id": 2, "nome": "Mouse", "preco": 80.50, "status": "PENDENTE"},
    {"id": 3, "nome": "Teclado", "preco": 150.00, "status": "PENDENTE"},
]

def gerar_qrcode(texto):
    qr = qrcode.make(texto)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

@app.route("/")
def index():
    return render_template("index.html", produtos=produtos)

@app.route("/pagamento/<int:id>")
def pagamento(id):
    produto = next((p for p in produtos if p["id"] == id), None)

    if not produto:
        return "Produto não encontrado"

    codigo_pix = f"PIX-FAKE-{produto['id']}-{produto['preco']}"
    qr_code = gerar_qrcode(codigo_pix)

    return render_template(
        "pagamento.html",
        produto=produto,
        codigo_pix=codigo_pix,
        qr_code=qr_code
    )

@app.route("/confirmar/<int:id>")
def confirmar(id):
    produto = next((p for p in produtos if p["id"] == id), None)
    
    if produto:
        produto["status"] = "PAGO"

    return redirect(url_for("index"))


@app.route("/editar/")
def editar():
    #produto = next((p for p in produtos if p["id"] == id), None)
    
    #if produto:
    #    produto["status"] = "PAGO"

    return render_template("editar.html")

if __name__ == "__main__":
    app.run(debug=True)