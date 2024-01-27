#!/usr/local/bin/python
# coding: latin-1
import csv
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random

def get_price(node):
    # Função para obter o preço do nó da página
    price_node = node.find('span', class_='andes-money-amount__fraction')
    cents_node = node.find('span', class_='andes-money-amount__decimals')
    
    if price_node is not None:
        price = price_node.text.strip()
        if cents_node is not None:
            price += ',' + cents_node.text.strip()
        return price
    return None

def remove_duplicates(products):
    unique_products = []
    duplicate_products = []

    seen_titles = set()
    seen_descriptions = set()

    for product in products:
        title = product[3]
        description = product[8]
        value = product[26]

        # Verificar se o título e descrição já foram vistos
        if (title, description) in seen_titles and (title, value) in seen_descriptions:
            duplicate_products.append(product)
        else:
            seen_titles.add((title, description))
            seen_descriptions.add((title, value))
            unique_products.append(product)

    return unique_products, duplicate_products


i = 1

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0'}
termo_busca = input("Digite o termo de busca: ")
tags = input("Digite as tags separadas por vírgulas: ").split(',')
categoria = input("Digite a categoria dos produtos: ")

# Pergunta sobre o termo de substituição
termo_substituicao = input("Digite o termo para substituir 'MercadoLivre' (ou pressione Enter para não substituir): ")
termo_substituicao = termo_substituicao.strip()

base_url = f"https://lista.mercadolivre.com.br/{termo_busca}"

# Caminho e nome do arquivo CSV
nome_arquivo = f"dados_produtos_ml_{termo_busca[:10]}.csv"
caminho_arquivo = os.path.abspath(nome_arquivo)

# Valores padrão do WooCommerce
published_default = '1'  # Publicado, 0 para Não Publicado
is_featured_default = '0'  # Não é destaque
visibility_default = 'visible'  # Visível no catálogo
short_description_default = ''  # Descrição curta em branco
date_sale_price_starts_default = ''  # Data de início da promoção em branco
date_sale_price_ends_default = ''  # Data de término da promoção em branco
tax_status_default = 'none'  # Não Tributável
tax_class_default = ''  # Classe de imposto em branco
in_stock_default = '1'  # Em estoque
stock_default = ''  # Quantidade em estoque em branco
low_stock_amount_default = ''  # Quantidade baixa em estoque em branco
backorders_allowed_default = 'no'  # Backorders não permitidos
sold_individually_default = 'yes'  # Vendido individualmente
weight_default = ''  # Peso em branco
length_default = ''  # Comprimento em branco
width_default = ''  # Largura em branco
height_default = ''  # Altura em branco
allow_customer_reviews_default = 'no'  # Avaliações de clientes não permitidas
purchase_note_default = ''  # Nota de compra em branco
shipping_class_default = ''  # Classe de envio em branco
download_limit_default = ''  # Limite de download em branco
download_expiry_days_default = ''  # Dias de expiração do download em branco
parent_default = ''  # Produto pai em branco
grouped_products_default = ''  # Produtos agrupados em branco
upsells_default = ''  # Upsells em branco
cross_sells_default = ''  # Cross-sells em branco
external_url_default = ''  # URL externa em branco
button_text_default = ''  # Texto do botão em branco
position_default = ''  # Posição em branco
attribute_name_default = ''  # Nome do atributo em branco
attribute_value_default = ''  # Valor do atributo em branco
attribute_visible_default = ''  # Visibilidade do atributo em branco
attribute_global_default = ''  # Global do atributo em branco
attribute_default_default = ''  # Valor padrão do atributo em branco

# Listas para armazenar produtos e duplicatas
products = []

with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
    writer = csv.writer(arquivo_csv, delimiter=',')
    writer.writerow([
        'ID', 'Type', 'SKU', 'Name', 'Published', 'Is featured?', 'Visibility in catalog', 'Short description',
        'Description', 'Date sale price starts', 'Date sale price ends', 'Tax status', 'Tax class', 'In stock?',
        'Stock', 'Low stock amount', 'Backorders allowed?', 'Sold individually?', 'Weight (kg)', 'Length (cm)',
        'Width (cm)', 'Height (cm)', 'Allow customer reviews?', 'Purchase note', 'Sale price', 'Regular price',
        'Categories', 'Tags', 'Shipping class', 'Images', 'Download limit', 'Download expiry days', 'Parent',
        'Grouped products', 'Upsells', 'Cross-sells', 'External URL', 'Button text', 'Position', 'Attribute 1 name',
        'Attribute 1 value(s)', 'Attribute 1 visible', 'Attribute 1 global', 'Attribute 1 default', 'Video'
    ])

    while True:
        try:
            page = requests.get(base_url, headers=headers)
            soup = BeautifulSoup(page.text, "html.parser")

            for div in soup.find_all('div', class_='ui-search-result__content-wrapper'):
                produto = div.find('h2', class_='ui-search-item__title')
                link = div.find("a", class_="ui-search-link")

                # Obter preço usando a função get_price
                valor_desconto_str = get_price(div)

                imagens = []
                video = ''

                frete_gratis = bool(div.find("p", class_="ui-search-item__shipping ui-search-item__shipping--free"))

                if link is not None:
                    response_produto = requests.get(link['href'], headers=headers)
                else:
                    continue  # Pula para a próxima iteração do loop

                site_produto = BeautifulSoup(response_produto.text, 'html.parser')
                descricao = site_produto.find('p', class_='ui-pdp-description__content')

                if descricao:
                    # Substituir todas as variações de "MercadoLivre" por "SoftArena" se o termo de substituição for informado
                    if termo_substituicao:
                        descricao_text = '<h1>' + produto.text + '</h1>\n\n' + descricao.text.strip().replace(termo_substituicao, "SoftArena")
                    else:
                        descricao_text = '<h1>' + produto.text + '</h1>\n\n' + descricao.text.strip()
                else:
                    # Quando não encontrar uma descrição, inserir o título do produto
                    descricao_text = '<h1>' + produto.text + '</h1>\n\n' + produto.text

                # Buscar imagens dentro do bloco do produto
                imagem_tags = site_produto.find_all('img', class_='ui-pdp-image ui-pdp-gallery__figure__image')
                
                for imagem in imagem_tags:
                    if 'data-zoom' in imagem.attrs:
                        imagens.append(imagem['data-zoom'])

                imagens_str = ', '.join(imagens)

                sku = site_produto.find('span', class_='ui-pdp-buybox__sku-value')
                if sku:
                    sku = sku.get_text(strip=True, separator='\n')
                else:
                    sku = '' + ''.join(random.choices('6789', k=13))

                writer.writerow([
                    i, 'simple', sku, produto.text, published_default, is_featured_default, visibility_default,
                    short_description_default, descricao_text, date_sale_price_starts_default,
                    date_sale_price_ends_default, tax_status_default, tax_class_default, in_stock_default,
                    stock_default, low_stock_amount_default, backorders_allowed_default, sold_individually_default,
                    weight_default, length_default, width_default, height_default, allow_customer_reviews_default,
                    purchase_note_default, valor_desconto_str, valor_desconto_str, categoria, ', '.join(tags),
                    shipping_class_default, ', '.join(imagens), download_limit_default, download_expiry_days_default,
                    parent_default, grouped_products_default, upsells_default, cross_sells_default,
                    external_url_default, button_text_default, position_default, attribute_name_default,
                    attribute_value_default, attribute_visible_default, attribute_global_default,
                    attribute_default_default, video
                ])

                products.append([
                    i, 'simple', sku, produto.text, published_default, is_featured_default, visibility_default,
                    short_description_default, descricao_text, date_sale_price_starts_default,
                    date_sale_price_ends_default, tax_status_default, tax_class_default, in_stock_default,
                    stock_default, low_stock_amount_default, backorders_allowed_default, sold_individually_default,
                    weight_default, length_default, width_default, height_default, allow_customer_reviews_default,
                    purchase_note_default, valor_desconto_str, valor_desconto_str, categoria, ', '.join(tags),
                    shipping_class_default, ', '.join(imagens), download_limit_default, download_expiry_days_default,
                    parent_default, grouped_products_default, upsells_default, cross_sells_default,
                    external_url_default, button_text_default, position_default, attribute_name_default,
                    attribute_value_default, attribute_visible_default, attribute_global_default,
                    attribute_default_default, video
                ])

                print('Código: ' + str(i) + ', Produto: ' + produto.text + ', Valor: ' + str(valor_desconto_str))
                print("==========================")

                if link:
                    print('Link: ' + link['href'])

                if descricao_text:
                    print('Descrição do produto: ' + descricao_text)
                else:
                    print('Descrição do produto não encontrada.')

                if imagens:
                    print('Imagens: ' + ', '.join(imagens))
                else:
                    print('Nenhuma imagem encontrada.')

                if video:
                    print('Video: ' + video)

                if frete_gratis:
                    print('Frete grátis')

                if sku:
                    print('SKU: ' + sku)

                if tags:
                    print('Tags: ' + ', '.join(tags))
                else:
                    print('Nenhuma tag encontrada.')

                i += 1

            next_link = soup.select_one("a.andes-pagination__link:-soup-contains(Seguinte)")

            if not next_link:
                break

            next_url = urljoin(base_url, next_link['href'])
            base_url = next_url

            # Aguardar um tempo aleatório entre 0.5 e 2.5 segundos entre as solicitações para evitar o bloqueio por sobrecarga no servidor
            time.sleep(random.uniform(0.5, 2.5))

        except ConnectionError as e:
            print("Ocorreu um erro de conexão:", e)

            print("Arquivo CSV salvo com sucesso:")
            print(caminho_arquivo)

            break

# Remover produtos duplicados
unique_products, duplicate_products = remove_duplicates(products)

# Exibir a quantidade de produtos duplicados e quais foram eles
print(f"Quantidade de produtos duplicados encontrados: {len(duplicate_products)}")
print("Produtos duplicados:")
for duplicate in duplicate_products:
    print(duplicate)

print("Arquivo CSV salvo com sucesso:")
print(caminho_arquivo)
