# 🚀 Sager_ONS  

**Sistema para baixar as planilhas do SAGER ONS - (Não Oficial)**  
📢 *O ONS ainda está desenvolvendo uma API oficial para essa funcionalidade.*  

## 📌 Sobre o projeto  

O **Sager_ONS** é um sistema automatizado para baixar planilhas do SAGER ONS. Ele facilita a extração de dados sem a necessidade de interação manual, útil para análises e automação de processos.  

## ⚙️ Como funciona  

1. Acesse o **SAGER ONS - Relatório Geral** no site oficial.  
2. Abra o **modo inspecionar** do navegador (Aba "Redes" ou "Network").  
3. Baixe manualmente uma planilha e identifique o **ID dos conjuntos de dados**.  
4. Configure o arquivo `.env` com suas credenciais:  

   ```ini
   EMAIL=seu_email_aqui
   SENHA=sua_senha_aqui
    ```
## Escolha o tipo de relatório (modifique no código conforme necessário):

tipoRelatorio: 1 → Relatório Geral

tipoRelatorio: 2 → Relatório de Geração de Referência

Execute o script para baixar os arquivos automaticamente.

## 🛠️ Tecnologias utilizadas
Python

Requests (para requisições HTTP)

Pandas (para manipulação de dados)

Dotenv (para gerenciar variáveis de ambiente)

📌 Requisitos
Antes de rodar o projeto, instale as dependências:

 ```ini
pip install -r requirements.txt
 ```
## ▶️ Como executar
 ```ini
python main.py
 ```
## 🖼 Exemplos
Aqui estão algumas imagens demonstrando a extração dos IDs e o funcionamento do sistema:




![image](https://github.com/user-attachments/assets/a0ae5e99-8567-46eb-b01a-fc1055022603)


![image](https://github.com/user-attachments/assets/8e0aa050-c12c-4e5c-a71f-92603e667812)


![image](https://github.com/user-attachments/assets/89eabf52-6fdf-4c7d-9a66-5749e25dea4f)



![image](https://github.com/user-attachments/assets/321476d8-095f-4ca3-b425-c60ba0db0dc0)



![image](https://github.com/user-attachments/assets/2285f643-3088-4ddb-bfaf-7b3710325619)

Quando você gerar a planilha do conjunto vai aparecer o ID idsConjuntos, e você precisa alimentar no codigo


tipoRelatorio: 1 igual a Relatorio Geral

tipoRelatorio: 2 igual a Relatorio Geração de Referencia




