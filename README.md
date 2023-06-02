# Script de Web Scraping de Produtos do Mercado Livre

Este é um script escrito em Python para realizar web scraping de produtos no site do Mercado Livre. O objetivo é extrair informações sobre os produtos, como título, preço, descrição, imagens, tags e SKU, e salvá-las em um arquivo CSV para uso posterior.

## Funcionalidades

- O script acessa a página de busca do Mercado Livre para obter uma lista de produtos relacionados a um determinado termo de pesquisa.
- Utiliza a biblioteca BeautifulSoup para analisar o HTML da página e extrair as informações desejadas.
- O script percorre os resultados da pesquisa, coletando informações como título, preço, descrição, imagens, tags e SKU de cada produto.
- Realiza algumas transformações nos dados para formatá-los adequadamente antes de escrevê-los no arquivo CSV.
- Verifica se as imagens têm um tamanho mínimo e se o conteúdo é uma imagem válida.
- Aplica um desconto de 12% ao preço original do produto.
- Gera um SKU aleatório para os produtos que não possuem SKU no site.
- Salva as informações coletadas no arquivo CSV, seguindo uma estrutura pré-definida de colunas.
- O script lida com várias páginas de resultados, navegando para a próxima página até que não haja mais páginas disponíveis.
- Inclui um mecanismo de espera de 2 segundos entre as solicitações para evitar bloqueio por sobrecarga no servidor.

## Como usar o script

1. Certifique-se de ter o Python instalado em seu sistema.
2. Clone o repositório e navegue até o diretório onde o script está localizado.
3. Instale as bibliotecas necessárias especificadas no código (`requests`, `beautifulsoup4`, `csv`).
4. Execute o script usando o comando `python nome_do_script.py`.
5. Aguarde o processamento das páginas e a criação do arquivo CSV.
6. O arquivo CSV será salvo no mesmo diretório do script com o nome `dados_produtos_ml_texturas.csv`.

## Observações

- O script foi desenvolvido para extrair informações de produtos relacionados a texturas do V-Ray no Mercado Livre, mas pode ser adaptado para outras categorias de produtos ou sites semelhantes.
- É importante respeitar os termos de uso e políticas de scraping do site em questão ao utilizar este script.
- O código inclui comentários detalhados explicando as diferentes partes e funcionalidades do script.
- Sinta-se à vontade para modificar o código para atender às suas necessidades específicas.

## Disclaimer

Este script foi desenvolvido apenas para fins educacionais e não deve ser usado para fins comerciais ou violar os termos de serviço de qualquer site. O scraping de sites pode ser uma atividade legalmente questionável ou proibida, portanto, use-o com responsabilidade e verifique as políticas e termos de uso do site antes de realizar qualquer ação de scraping.
