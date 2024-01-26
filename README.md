# Script de Web Scraping de Produtos do Mercado Livre

Este é um script escrito em Python para realizar web scraping de produtos no site do Mercado Livre. O objetivo é extrair informações sobre os produtos, como título, preço, descrição, imagens, tags e SKU, e salvá-las em um arquivo CSV para uso posterior.

Ele gera o arquivo csv no formato de produtos que o woocomerce usa para fazer importação dos mesmos. Tentei deixar o script comentado o máximno possível.

## Funcionalidades

- **Obtenção de Preços:** O script utiliza a função `get_price` para extrair o preço dos produtos, considerando valores e centavos quando disponíveis.

- **Coleta de Informações:** Percorre os resultados da pesquisa no Mercado Livre, coletando informações como título, preço, descrição, imagens, tags e SKU de cada produto.

- **Transformações nos Dados:** Realiza transformações nos dados, aplicando um desconto de 12% ao preço original e gerando SKUs aleatórios para produtos sem SKU no site.

- **Salvamento em CSV:** As informações coletadas são salvas em um arquivo CSV seguindo uma estrutura predefinida de colunas, compatível com o formato utilizado pelo WooCommerce.

- **Navegação entre Páginas:** Lida com várias páginas de resultados, navegando para a próxima página até que não haja mais disponíveis.

- **Espera entre Solicitações:** Inclui um mecanismo de espera de 0.5 a 2.5 segundos entre as solicitações para evitar bloqueio por sobrecarga no servidor.

- **Exibição de Informações:** Exibe no console informações relevantes sobre cada produto, como código, título, valor com desconto, link, descrição, imagens, vídeo, frete grátis, SKU e tags.

- **Adaptação para SoftArena:** Substitui variações de "MercadoLivre" por "SoftArena" na descrição dos produtos.

## Como usar o script

1. Certifique-se de ter o Python instalado em seu sistema.
2. Clone o repositório e navegue até o diretório onde o script está localizado.
3. Instale as bibliotecas necessárias especificadas no código (`requests`, `beautifulsoup4`, `csv`).
4. Execute o script usando o comando `python nome_do_script.py`.
5. Aguarde o processamento das páginas e a criação do arquivo CSV.
6. O arquivo CSV será salvo no mesmo diretório do script com o nome `dados_produtos_ml_texturas.csv`.

## Observações

- O script foi originalmente desenvolvido para extrair informações de texturas do V-Ray no Mercado Livre, mas pode ser adaptado para outras categorias de produtos ou sites semelhantes.
- O código inclui comentários detalhados explicando as diferentes partes e funcionalidades.
- Este script foi desenvolvido para fins práticos e de automação. Utilize-o com responsabilidade e sempre respeite os termos de serviço do site de origem.

## "Disclaimer".

Sabe esse blablabla que: 

"Este script foi desenvolvido apenas para fins educacionais e não deve ser usado para fins comerciais ou violar os termos de serviço de qualquer site. O scraping de sites pode ser uma atividade legalmente questionável ou proibida, portanto, use-o com responsabilidade e verifique as políticas e termos de uso do site antes de realizar qualquer ação de scraping."

Esquece isso, é pra torá o pau mesmo. Esse script foi escrito para tirar proveito das técnicas de scraping. Pra economizar tempo e dinheiro que seria gasto cadastrando produtos que vc já encontra tudo mastigado no ML.
