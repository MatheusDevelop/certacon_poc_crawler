from selenium.webdriver import Chrome 
from selenium.webdriver import ChromeOptions 
from selenium.webdriver.common.by import By
import requests
chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')

driver = Chrome(options=chrome_options)

apiUrl = "http://localhost:8080/documentos"
url = "https://www.vriconsulting.com.br/guias/guiasIndex.php?idGuia=22"
print("Navegando ao site...")
driver.get(url)
print("Sincronizando...")

tabela = driver.find_element(By.XPATH, '//*[@id="corpoGuia"]/table[1]/tbody')

linhas = tabela.find_elements(By.TAG_NAME, "tr")

dados_da_tabela = []
print("Sincronizando tabela")
for linha in linhas:
    cells = linha.find_elements(By.TAG_NAME, "td")
    
    if len(cells) == 8:
        n = cells[0].text
        campo = cells[1].text
        descricao = cells[2].text
        tipo = cells[3].text
        tamanho = cells[4].text
        decimais = cells[5].text
        entrada = cells[6].text
        saida = cells[7].text

        
        dado = {
            "Numero": n,
            "Campo": campo,
            "Descricao": descricao,
            "Tipo": tipo,
            "Tamanho": tamanho,
            "Decimais": decimais,
            "Entrada": entrada,
            "Saida":saida
        }
        
        dados_da_tabela.append(dado)

driver.quit()
print("Sincronizando com banco de dados...")
response = requests.post(apiUrl,json= dados_da_tabela)
if response.status_code == 201:
    print("Sincronização bem-sucedida.")
    print("Você já pode fechar esse programa.")
else:
    print("Falha na sincronização.")
    print("Código de status:", response.status_code)
    print("Resposta do servidor:", response.text)