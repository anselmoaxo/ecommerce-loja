from pixqrcodegen import Payload


nome = "Anselmo Xavier"
chavepix = "anselmo.cstecnologia@gmail.com"
valor = "1.00"
cidade = "Guarulhos"
txtId = "Ecommerce_AXO"

# Parâmetros necessários
payload = Payload(nome, chavepix, valor, cidade, txtId)

# Chamando a função responsável para gerar a Payload Pix e o QR Code
payload.gerarPayload()
