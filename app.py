#Codigo baixar planilhas
# -*- encoding: utf-8 -*-
import requests
import pandas as pd
import os
import time
import getpass
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Carregar variáveis do arquivo .env
load_dotenv()

# Obtém a data do dia anterior
ontem = datetime.now() - timedelta(days=1)
data_inicial = ontem.strftime("%Y-%m-%dT00:00:00.000Z")
data_final = ontem.strftime("%Y-%m-%dT23:59:59.000Z")
data_arquivo = ontem.strftime("%m%d")  # Formato MMDD para nome do arquivo
ano_atual = ontem.strftime("%Y")  # Ano atual

# Mapeamento das subestações para tags pegar os nomes do conjunto do SINapse e adicionar as tag´s da subestação
SE_TAG_MAP = {
    'Conj. xxxx': 'xxxx',
    'Conj. xxxx2': 'xxxx2',
}

class SinapseONS:
    def __init__(self):
        self.ons_user = os.getenv("ONS_USER")
        self.ons_pass = os.getenv("ONS_PASS")
        self.session = requests.Session()
        self.access_token = None
        self.usuario_sistema = getpass.getuser()  # Obtém o nome do usuário do sistema

    def autenticar(self):
        """Autentica no portal ONS e obtém o access token mantendo a sessão ativa."""
        login_url = "https://pops.ons.org.br/ons.pop.federation/?ReturnUrl=https://sinapse.ons.org.br/autenticacao/login"

        with self.session as s:
            response = s.get(login_url)

            headers = {
                'Origin': 'https://pops.ons.org.br',
                'Pragma': 'no-cache',
                'Referer': login_url,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            }

            data = {
                'username': self.ons_user,
                'password': self.ons_pass,
                'submit.Signin': 'Entrar',
                'CountLogin': '0',
            }

            response = s.post(login_url, headers=headers, data=data)
            
            if response.status_code != 200:
                print("❌ Erro ao autenticar: Verifique usuário e senha.")
                return False

            print("✅ Autenticação realizada com sucesso.")

            # Obter token de acesso
            token_url = "https://pops.ons.org.br/ons.pop.federation/oauth2/token"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://pops.ons.org.br',
                'Referer': 'https://pops.ons.org.br/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            }
            data = {
                'grant_type': 'password',
                'client_id': 'SINAPSE',
                'username': self.ons_user,
                'password': self.ons_pass
            }

            response = s.post(token_url, headers=headers, data=data)

            if response.status_code == 200:
                self.access_token = response.json()['access_token']
                print(f"✅ Token obtido com sucesso: {self.access_token[:10]}...")

                # Aguarda 5 segundos antes de fazer qualquer outra requisição
                time.sleep(5)
                return True
            else:
                print(f"❌ Erro ao obter token: {response.status_code} - {response.text}")
                return False

    def criar_pasta_relatorio(self, subestacao, tipo_relatorio):
        """Cria o diretório correto para armazenar os relatórios filtrados."""
        base_path = os.path.join(
            f"C:\\Users\\{self.usuario_sistema}\\",
            #f"{subestacao}_SAGER",
            #f"{ano_atual}_{subestacao}_SAGER",
            #f"{ano_atual}-{tipo_relatorio}-SINapse"
        )
        os.makedirs(base_path, exist_ok=True)
        return base_path

    def baixar_csv(self, url, nome, tipo_relatorio):
        """Baixa um relatório da API do SINAPSE ONS e salva os dados separados por subestação."""
        if not self.access_token:
            print("Erro: Nenhum token disponível. Faça login primeiro.")
            return None

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Referer': 'https://sinapse.ons.org.br/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }

        cookies = self.session.cookies.get_dict()

        payload = {
            "origem": None,
            "destino": None,
            "status": None,
            #"periodoInicial": data_inicial,
            #"periodoFinal": data_final,
            "periodoInicial": "2025-02-01T00:00:00.000Z",
            "periodoFinal": "2025-02-23T23:59:59.000Z",
            "mensagem": ""
        }
        #print(payload)
        # Inclua também o cabeçalho 'perfil-selecionado' conforme o exemplo (ajuste se necessário)
        headers.update({
                'perfil-selecionado': 'Apurador%20Agente%2FAGENTES%2F189%2FVOLTALIA'
            })

        print(f"Baixando {nome}...")

        response = self.session.post(url, json=payload, headers=headers, cookies=cookies, stream=True)

        if response.status_code == 200:
            temp_path = os.path.join(os.getcwd(), f"temp_{nome}.csv")

            with open(temp_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

            df = pd.read_csv(temp_path, delimiter=";", encoding="utf-8")

            os.remove(temp_path)  # Remove o arquivo temporário após processamento

            # Filtrar e salvar cada subestação separadamente
            for chave, valor in SE_TAG_MAP.items():
                df_filtrado = df[df["Mensagem"].str.contains(chave, na=False, case=False)]
                
                if not df_filtrado.empty:
                    pasta_destino = self.criar_pasta_relatorio(valor, tipo_relatorio)
                    file_destino = os.path.join(pasta_destino, f"{ano_atual}_{valor}_{tipo_relatorio}_{data_arquivo}.csv")

                    df_filtrado.to_csv(file_destino, index=False, sep=";", encoding="utf-8-sig")
                    print(f"📂 Dados da subestação '{chave}' salvos em: {file_destino}")

        else:
            print(f"❌ Erro ao baixar '{nome}': {response.status_code} - {response.text}")

    def baixar_relatorios(self):
        """Baixa os relatórios analítico e simplificado."""
        urls = {
            "analitico": "https://api.sinapse.ons.org.br/api/solicitacao/pesquisa/exportar-analitico",
            "simplificado": "https://api.sinapse.ons.org.br/api/solicitacao/pesquisa/exportar"
        }

        self.baixar_csv(urls["analitico"], "Relatório Analítico", "HC")
        self.baixar_csv(urls["simplificado"], "Relatório Simplificado", "HS")

# Criar a instância e executar o processo
if __name__ == "__main__":
    ons = SinapseONS()
    if ons.autenticar():
        ons.baixar_relatorios()
