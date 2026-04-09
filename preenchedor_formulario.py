from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# ==========================================
# ⚙️ VARIÁVEIS GLOBAIS (Edite seus dados aqui)
# ==========================================
MARCAR_RECIBO_EMAIL = True
NOME_PROFESSOR = "Geison Antunes Branco Koepp"
TIPO_ORIENTADOR = "Tecnologias Educacionais" # Ou "Laboratório Maker"
REGIONAL = "GRANDE FPOLIS"
ESCOLA = "EEB VICENTE SILVEIRA"
# ==========================================

def preencher_formulario():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    print("Conectando ao Chrome na porta 9222...")
    try:
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)
    except Exception:
        print("Erro: Não foi possível conectar ao Chrome. Certifique-se de abri-lo no modo de depuração.")
        return

    print("\n--- INICIANDO PREENCHIMENTO DO FORMULÁRIO ---")

    try:
        # PÁGINA 1
        print("\n[Página 1] Preenchendo dados iniciais...")
        
        # 1. Marcar checkbox de e-mail (se existir e estiver configurado)
        if MARCAR_RECIBO_EMAIL:
            # Busca o checkbox pelo 'role'
            checkboxes = driver.find_elements(By.XPATH, "//div[@role='checkbox']")
            if checkboxes:
                checkbox = checkboxes[0]
                # Só clica se não estiver marcado
                if checkbox.get_attribute("aria-checked") == "false":
                    print(" -> Marcando envio de recibo por e-mail...")
                    driver.execute_script("arguments[0].click();", checkbox)
                    time.sleep(0.5)

        # 2. Preencher Nome
        print(f" -> Inserindo nome: {NOME_PROFESSOR}")
        input_nome = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
        input_nome.clear()
        input_nome.send_keys(NOME_PROFESSOR)
        time.sleep(0.5)

        # 3. Marcar Radio Button (Tipo de Orientador)
        print(f" -> Selecionando área: {TIPO_ORIENTADOR}")
        radio_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@role='radio' and @data-value='{TIPO_ORIENTADOR}']")))
        driver.execute_script("arguments[0].click();", radio_btn)
        time.sleep(0.5)

        # 4. Selecionar Dropdown (REGIONAL)
        print(f" -> Selecionando regional: {REGIONAL}")
        # Clica para abrir a lista
        lista_regional = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='listbox']")))
        driver.execute_script("arguments[0].click();", lista_regional)
        time.sleep(1) # Aguarda a animação do Google abrir as opções
        
        # Clica na opção desejada
        opcao_regional = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@role='option' and @data-value='{REGIONAL}']")))
        driver.execute_script("arguments[0].click();", opcao_regional)
        time.sleep(1)

        # 5. Clicar em Avançar
        print(" -> Clicando em Avançar...")
        btn_avancar = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Avançar']")))
        driver.execute_script("arguments[0].click();", btn_avancar)
        
        # PÁGINA 2
        print("\n[Página 2] Carregando seleção de escola...")
        time.sleep(3) # Pausa estratégica para a página 2 carregar totalmente
        
        # 6. Selecionar Dropdown (ESCOLA)
        print(f" -> Selecionando escola: {ESCOLA}")
        lista_escola = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='listbox']")))
        driver.execute_script("arguments[0].click();", lista_escola)
        time.sleep(1)
        
        opcao_escola = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@role='option' and @data-value='{ESCOLA}']")))
        driver.execute_script("arguments[0].click();", opcao_escola)
        time.sleep(1)

        # 7. Clicar em Avançar novamente
        print(" -> Clicando em Avançar...")
        btn_avancar_2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Avançar']")))
        driver.execute_script("arguments[0].click();", btn_avancar_2)
        
        time.sleep(2)
        
        # 8. Fim
        print("\n=======================================================")
        print("✅ FINALIZAÇÃO: O formulário foi preenchido com sucesso!")
        print("=======================================================")

    except Exception as e:
        print(f"\n❌ ERRO DURANTE O PROCESSO: O robô se perdeu.")
        print(f"Detalhe técnico: {str(e)}")

if __name__ == "__main__":
    preencher_formulario()
