from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# ==========================================
# ⚙️ VARIÁVEIS GLOBAIS (Edite seus dados aqui)
# ==========================================
MARCAR_RECIBO_EMAIL = True
NOME_PROFESSOR = "Geison Antunes Branco Koepp"
TIPO_ORIENTADOR = "Tecnologias Educacionais" 
REGIONAL = "GRANDE FPOLIS" 
ESCOLA = "EEB VICENTE SILVEIRA"
# ==========================================

def preencher_formulario():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    print("Conectando ao Chrome na porta 9222...")
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception:
        print("Erro: Não foi possível conectar ao Chrome. Certifique-se de abri-lo no modo de depuração.")
        return

    # --- FUNÇÕES DE SEGURANÇA CONTRA O GOOGLE FORMS ---
    def esperar_e_clicar(xpath, descricao, tempo_maximo=15):
        print(f" -> Ação: {descricao}...")
        for _ in range(int(tempo_maximo * 2)): 
            elementos = driver.find_elements(By.XPATH, xpath)
            visiveis = [el for el in elementos if el.is_displayed()]
            if visiveis:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", visiveis[0])
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", visiveis[0])
                    return True
                except:
                    pass
            time.sleep(0.5)
        raise Exception(f"O robô não encontrou o elemento: {descricao}")

    def selecionar_dropdown(xpath_caixa, valor_desejado, descricao):
        print(f" -> Ação: Abrindo {descricao} para buscar '{valor_desejado}'...")
        caixas = driver.find_elements(By.XPATH, xpath_caixa)
        caixa_visivel = next((c for c in caixas if c.is_displayed()), None)
                
        if not caixa_visivel:
            raise Exception(f"Não encontrou a caixa: {descricao}")
            
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", caixa_visivel)
        time.sleep(0.5)
        
        # Abre a caixa
        try:
            ActionChains(driver).move_to_element(caixa_visivel).click().perform()
        except:
            driver.execute_script("arguments[0].click();", caixa_visivel)
            
        time.sleep(2) # Espera a lista flutuante abrir completamente
        
        # Procura a opção pelo valor (data-value)
        xpath_opcao = f"//div[@role='option' and @data-value='{valor_desejado}']"
        opcoes = driver.find_elements(By.XPATH, xpath_opcao)
        
        if opcoes:
            opcao_alvo = opcoes[-1] # Pega a última caso existam opções ocultas de páginas anteriores
            
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", opcao_alvo)
            time.sleep(0.5)
            
            # O TRUQUE MESTRE: Simulando o 'apertar' e 'soltar' do mouse fisicamente no JavaScript
            script_clique_supremo = """
                var el = arguments[0];
                el.dispatchEvent(new MouseEvent('mousedown', {bubbles: true, cancelable: true, view: window}));
                el.dispatchEvent(new MouseEvent('mouseup', {bubbles: true, cancelable: true, view: window}));
                el.click();
            """
            driver.execute_script(script_clique_supremo, opcao_alvo)
            time.sleep(1.5) # Aguarda a caixa fechar
            return True
        else:
            raise Exception(f"A opção '{valor_desejado}' não existe na lista. Verifique a ortografia exata.")

    def esperar_e_digitar(xpath, texto, descricao, tempo_maximo=15):
        print(f" -> Ação: Digitando em {descricao}...")
        for _ in range(int(tempo_maximo * 2)):
            elementos = driver.find_elements(By.XPATH, xpath)
            visiveis = [el for el in elementos if el.is_displayed()]
            if visiveis:
                try:
                    el = visiveis[0]
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                    time.sleep(0.5)
                    actions = ActionChains(driver)
                    actions.move_to_element(el).click().pause(0.3)
                    actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE)
                    actions.send_keys(texto).perform()
                    return True
                except Exception:
                    pass
            time.sleep(0.5)
        raise Exception(f"O robô não conseguiu digitar no campo: {descricao}")
    # ---------------------------------------------------

    print("\n--- INICIANDO PREENCHIMENTO DO FORMULÁRIO ---")

    try:
        # ========================================================
        # [0] FOCAR NA ABA CORRETA AUTOMATICAMENTE
        # ========================================================
        aba_form = None
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if "docs.google.com/forms" in driver.current_url.lower():
                aba_form = handle
                break
                
        if not aba_form:
            print("❌ ERRO: Nenhuma aba com o Google Forms foi encontrada!")
            return
        time.sleep(1)

        # ========================================================
        # ORDEM DE EXECUÇÃO EXATA SOLICITADA
        # ========================================================

        # 1- deve marcar o ckeckbox
        if MARCAR_RECIBO_EMAIL:
            checkboxes = driver.find_elements(By.XPATH, "//div[@role='checkbox']")
            if checkboxes and checkboxes[0].is_displayed() and checkboxes[0].get_attribute("aria-checked") == "false":
                esperar_e_clicar("//div[@role='checkbox']", "Caixa de recibo de e-mail")

        # 2- deve preencher com o nome
        esperar_e_digitar("//div[@role='listitem']//input[@type='text']", NOME_PROFESSOR, "Campo de Nome")

        # 3- marcar checkbox de Tecnologias Educacionais
        esperar_e_clicar(f"//div[@data-value='{TIPO_ORIENTADOR}']", f"Opção: {TIPO_ORIENTADOR}")

        # 4- selecionar ou preencher com "GRANDE FPOLIS"
        selecionar_dropdown("//div[@role='listbox']", REGIONAL, "Menu de Regionais")

        # 5- clicar no botão Avançar
        esperar_e_clicar("//span[text()='Avançar']", "Botão Avançar (Página 1)")
        
        # Pausa para o carregamento da próxima página
        time.sleep(3) 
        
        # 6- selecionar ou preencher com "EEB VICENTE SILVEIRA"
        selecionar_dropdown("//div[@role='listbox']", ESCOLA, "Menu de Escolas")

        # 7- clicar no botão avançar
        # O botão da última página pode se chamar "Enviar", então buscamos por ambos
        esperar_e_clicar("//span[text()='Avançar' or text()='Enviar']", "Botão Avançar/Enviar (Página 2)")
        time.sleep(2)

        # 8- fim e exibir a mensagem de alerta no console de Finalização
        print("\n=======================================================")
        print("✅ FINALIZAÇÃO: O formulário foi preenchido com sucesso e está na etapa final!")
        print("=======================================================")

    except Exception as e:
        print(f"\n❌ ERRO DURANTE O PROCESSO:")
        print(str(e))

if __name__ == "__main__":
    preencher_formulario()