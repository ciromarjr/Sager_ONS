#Sager_ONS

Sistema para baixar as planilhas do SAGER ONS - Não Oficial
(O ONS ainda está desenvolvendo uma API oficial para essa funcionalidade.)

📌 Descrição
Este sistema permite o download automatizado das planilhas do SAGER ONS, extraindo os dados diretamente do sistema do ONS. Como a API oficial ainda está em desenvolvimento, o processo requer a obtenção manual dos IDs dos conjuntos para gerar os relatórios desejados.

🚀 Como Usar
1️⃣ Configuração Inicial
Obtenha seu ID de conjunto:

Acesse o sistema SAGER ONS - Relatório Geral

Abra o modo Inspecionar do navegador (F12 → Aba "Rede" ou "Network")

Baixe uma planilha manualmente e identifique o ID dos conjuntos (idsConjuntos) que será necessário no código

Configuração do arquivo .env

Adicione seu e-mail e senha de acesso ao ONS no arquivo .env:

ini
Copiar
Editar
EMAIL=seuemail@exemplo.com
SENHA=suasenha
2️⃣ Executando o Sistema
Após configurar o .env, execute o sistema e forneça os IDs dos conjuntos obtidos anteriormente.

3️⃣ Tipos de Relatório
tipoRelatorio: 1 → Relatório Geral

tipoRelatorio: 2 → Relatório de Geração de Referência

🖼 Exemplos
Aqui estão algumas imagens demonstrando a extração dos IDs e o funcionamento do sistema:



![image](https://github.com/user-attachments/assets/a0ae5e99-8567-46eb-b01a-fc1055022603)


![image](https://github.com/user-attachments/assets/8e0aa050-c12c-4e5c-a71f-92603e667812)


![image](https://github.com/user-attachments/assets/89eabf52-6fdf-4c7d-9a66-5749e25dea4f)



![image](https://github.com/user-attachments/assets/321476d8-095f-4ca3-b425-c60ba0db0dc0)



![image](https://github.com/user-attachments/assets/2285f643-3088-4ddb-bfaf-7b3710325619)

Quando você gerar a planilha do conjunto vai aparecer o ID idsConjuntos, e você precisa alimentar no codigo


tipoRelatorio: 1 igual a Relatorio Geral

tipoRelatorio: 2 igual a Relatorio Geração de Referencia




