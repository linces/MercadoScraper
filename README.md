# Script de Web Scraping de Produtos do Mercado Livre

Este é um script escrito em Python para realizar web scraping de produtos no site do Mercado Livre. O objetivo é extrair informações sobre os produtos, como título, preço, descrição, imagens, tags e SKU, e salvá-las em um arquivo CSV para uso posterior.

Ele gera o arquivo csv no formato de produtos que o woocomerce usa para fazer importação dos mesmos. Tentei deixar o script comentado o máximno possível.

## Funcionalidades

- **Obtenção de Preços:** O script utiliza a função `get_price` para extrair o preço dos produtos, considerando valores e centavos quando disponíveis.

- **Coleta de Informações:** Percorre os resultados da pesquisa no Mercado Livre, coletando informações como título, preço, descrição, imagens, tags e SKU de cada produto.

- **Salvamento em CSV:** As informações coletadas são salvas em um arquivo CSV seguindo uma estrutura predefinida de colunas, compatível com o formato utilizado pelo WooCommerce.

- **Navegação entre Páginas:** Lida com várias páginas de resultados, navegando para a próxima página até que não haja mais disponíveis.

- **Espera entre Solicitações:** Inclui um mecanismo de espera de 0.5 a 2.5 segundos entre as solicitações para evitar bloqueio por sobrecarga no servidor.

- **Exibição de Informações:** Exibe no console informações relevantes sobre cada produto, como código, título, valor com desconto, link, descrição, imagens, vídeo, frete grátis, SKU e tags.



## Uso do Script de Web Scraping para Produtos do Mercado Livre

#### 1. **Parâmetros de Entrada:**
   - **Termo de Busca:** Um termo específico para pesquisar produtos no Mercado Livre.
   - **Tags:** Palavras-chave adicionais separadas por vírgulas para categorizar os produtos.
   - **Categoria:** A categoria à qual os produtos pertencem.
   - **Substituição de Termo (Opcional):** Um termo para substituir "MercadoLivre" na descrição dos produtos.

#### 2. **Execução do Script:**
   - O script é executado em um ambiente Python (certifique-se de ter o Python instalado).
   - Clone o repositório e navegue até o diretório onde o script está localizado.
   - Instale as bibliotecas necessárias (`requests`, `beautifulsoup4`, `csv`) especificadas no código.
   - Execute o script usando o comando `python nome_do_script.py`.
   - Durante a execução, o script solicitará que você insira o termo de busca, tags, categoria e, opcionalmente, um termo de substituição.

#### 3. **Saída do Script:**
   - Um arquivo CSV é gerado no mesmo diretório do script.
   - O arquivo CSV segue uma estrutura predefinida de colunas para importação no WooCommerce.
   - As informações extraídas incluem ID, tipo, SKU, nome, preço, descrição, imagens, tags, etc.

#### 4. **Customização:**
   - O código inclui comentários detalhados para facilitar a compreensão e modificações.
   - Pode ser adaptado para outras categorias de produtos ou sites semelhantes.

### Exemplo de Execução:

1. **Entrada:**
   - Termo de Busca: "câmera digital"
   - Tags: "tecnologia, fotografia"
   - Categoria: "Eletrônicos"
   - Substituição de Termo (Opcional):** Um termo para substituir "MercadoLivre" na descrição dos produtos.
 
2. **Execução:**
   - O script percorre o Mercado Livre, coleta informações sobre câmeras digitais e gera um arquivo CSV.

3. **Saída:**
   - Um arquivo CSV chamado `dados_produtos_ml_camera_digital.csv` é criado.

4. **Customização:**
   - Se necessário, ajuste as configurações padrão e estrutura das colunas conforme suas necessidades.


## "Disclaimer".

Sabe esse blablabla que: 

"Este script foi desenvolvido apenas para fins educacionais e não deve ser usado para fins comerciais ou violar os termos de serviço de qualquer site. O scraping de sites pode ser uma atividade legalmente questionável ou proibida, portanto, use-o com responsabilidade e verifique as políticas e termos de uso do site antes de realizar qualquer ação de scraping."

Esquece isso, é pra torá o pau mesmo. Esse script foi escrito para tirar proveito das técnicas de scraping. Pra economizar tempo e dinheiro que seria gasto cadastrando produtos que vc já encontra tudo mastigado no ML.
