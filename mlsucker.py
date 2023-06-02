#!/usr/local/bin/python
# coding: latin-1
import csv
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random

def get_value(node, nome, valor_default=''):
    campo = node.find(nome, class_="price-tag-fraction")
    if campo is None:
        return valor_default
    return campo.text

def get_cents(node, nome, valor_default=''):
    campo = node.find(nome, class_="price-tag-cents")
    if campo is None:
        return valor_default
    return campo.text

def check_image_size(url):
    response = requests.head(url)
    content_type = response.headers.get('content-type')

    if 'image' not in content_type:
        return False

    if 'content-length' in response.headers:
        content_length = int(response.headers.get('content-length', 0))
        if content_length < 200:
            return False

    return True

i = 1

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0'}
base_url = "https://lista.mercadolivre.com.br/Texturas-vray"

# Caminho e nome do arquivo CSV
nome_arquivo = "dados_produtos_ml_texturas.csv"
caminho_arquivo = os.path.abspath(nome_arquivo)

# Valores padrão do WooCommerce
published_default = '0'  # Não publicado, 1 para Publicado
is_featured_default = '0'  # Não é destaque, obviamente "1" é destaque
visibility_default = 'visible'  # Visível no catálogo
short_description_default = ''  # Descrição curta em branco
date_sale_price_starts_default = ''  # Data de início da promoção em branco
date_sale_price_ends_default = ''  # Data de término da promoção em branco
tax_status_default = 'none'  # Não tributável
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
                valor = get_value(div, "span") + "," + get_cents(div, "span")
                valor_desconto = float(valor.replace('.', '').replace(',', '.')) * 0.88  # Aplica o desconto de 12%, aqui é uma decisão pessoal para o meu negócio, vc n precisa aplicar desconto algum.
                valor_desconto = "{:.2f}".format(valor_desconto).replace('.', ',')  # Formata o valor com duas casas decimais e vírgula
                imagens = []
                video = ''

                if div.find("p", class_="ui-search-item__shipping ui-search-item__shipping--free") is None:
                    frete_gratis = False
                else:
                    frete_gratis = True

                if link is not None:
                    response_produto = requests.get(link['href'], headers=headers)
                else:
                    continue  # Pula para a próxima iteração do loop

                site_produto = BeautifulSoup(response_produto.text, 'html.parser')
                descricao = site_produto.find('p', class_='ui-pdp-description__content')

                if descricao:
                    descricao_text = '<h1>' + produto.text + '</h1>\n\n' + descricao.text.strip().replace("MercadoLivre", "SoftArena").replace("Mercado Livre", "SoftArena").replace("MERCADO LIVRE", "SoftArena").replace("M E R C A D O L I V R E", "SoftArena")
                else:
                    descricao_text = '<h1>' + produto.text + '</h1>\n\nDescrição do produto não encontrada.'

                imagem_tags = site_produto.find_all('img', class_='ui-pdp-image')

                for imagem in imagem_tags:
                    if 'data-src' in imagem.attrs:
                        if 'youtube' in imagem['data-src']:
                            video = imagem['data-src']
                        elif not imagem['data-src'].endswith('.svg'):  # Verifica se o link não termina com ".svg"
                            width = int(imagem['width'])
                            height = int(imagem['height'])
                            if width >= 200 and height >= 200:
                                imagens.append(imagem['data-src'])

                imagens_str = ', '.join(imagens)

                if not imagens:
                    continue  # Pula para a próxima iteração do loop se nenhuma imagem atender aos requisitos

                tags = []  # Lista de tags vazia

                tags_div = site_produto.find('div', class_='ui-pdp-attributes__value-list')
                if tags_div:
                    tags_links = tags_div.find_all('a')
                    tags = [tag_link.text for tag_link in tags_links]

                sku = ''  # SKU vazio

                sku_span = site_produto.find('span', class_='ui-pdp-buybox__sku-value')
                if sku_span:
                    sku = sku_span.text.strip()
                else:
                    # Criar um código EAN aleatório para o SKU
                    sku = '' + ''.join(random.choices('3456789', k=13))
                    # sku = random.choices('3456789', k=13)

                if not tags:
                    tags = ['Texturas/Temas']  # Adicionar a tag padrão quando nenhuma tag for encontrada

                writer.writerow([
                    i, 'simple', sku, produto.text, '0', is_featured_default, visibility_default,
                    short_description_default, descricao_text, date_sale_price_starts_default,
                    date_sale_price_ends_default, tax_status_default, tax_class_default, in_stock_default,
                    stock_default, low_stock_amount_default, backorders_allowed_default, sold_individually_default,
                    weight_default, length_default, width_default, height_default, allow_customer_reviews_default,
                    purchase_note_default, valor_desconto, valor, 'Texturas/Temas', ', '.join(tags), shipping_class_default,
                    imagens_str, download_limit_default, download_expiry_days_default, parent_default,
                    grouped_products_default, upsells_default, cross_sells_default, external_url_default,
                    button_text_default, position_default, attribute_name_default, attribute_value_default,
                    attribute_visible_default, attribute_global_default, attribute_default_default, video
                ])

                print('Código: ' + str(i) + ', Produto: ' + produto.text + ', Valor: ' + valor_desconto)

                print("==========================")

                if link is not None:
                    print('Link: ' + link['href'])

                if descricao:
                    print('Descrição do produto: ' + descricao_text)
                else:
                    print('Descrição do produto não encontrada.')

                if imagens_str:
                    print('Imagens: ' + imagens_str)
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

            # Aguardar 2 segundos entre as solicitações para evitar o bloqueio por sobrecarga no servidor
            time.sleep(2)

        except Exception as e:
            print('Erro ao processar a página: ' + str(e))
            break

print('Arquivo CSV gerado com sucesso em: ' + caminho_arquivo)
