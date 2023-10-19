from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import requests

def sync_data_with_api(url, data):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.status_code
    except requests.exceptions.RequestException as e:
        print("Falha na sincronização.")
        print("Erro:", e)
        return None

def extract_table_data(driver):
    tabela = driver.find_element(By.XPATH, '//*[@id="corpoGuia"]/table[1]/tbody')
    linhas = tabela.find_elements(By.TAG_NAME, "tr")
    dados_da_tabela = []

    for linha in linhas:
        cells = linha.find_elements(By.TAG_NAME, "td")

        if len(cells) == 8:
            n, campo, descricao, tipo, tamanho, decimais, entrada, saida = [cell.text for cell in cells]

            dado = {
                "Numero": n,
                "Campo": campo,
                "Descricao": descricao,
                "Tipo": tipo,
                "Tamanho": tamanho,
                "Decimais": decimais,
                "Entrada": entrada,
                "Saida": saida
            }

            dados_da_tabela.append(dado)

    return dados_da_tabela

def main():
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--log-level=3');
    
    driver = Chrome(options=chrome_options)
    url = "https://www.vriconsulting.com.br/guias/guiasIndex.php?idGuia=22"
    print("Navegando ao site...")
    driver.get(url)
    print("Sincronizando...")

    dados_da_tabela = extract_table_data(driver)
    driver.quit()

    api_url = "http://localhost:8080/documents/sync"
    print("Sincronizando com banco de dados...")
    status_code = sync_data_with_api(api_url, dados_da_tabela)

    if status_code == 201:
        print("Sincronização bem-sucedida.")
        print("Você já pode fechar esse programa.")
    elif status_code is not None:
        print("Falha na sincronização.")
        print("Código de status:", status_code)

if __name__ == "__main__":
    main()
