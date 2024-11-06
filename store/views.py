import json

from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Product


@csrf_exempt
def webhook(request: HttpRequest) -> HttpResponse:
    """Handle webhook requests from Dialogflow."""
    if request.method == 'POST':
        req = json.loads(request.body)

        response_text = opcoes_intent(req)

        return JsonResponse({
            "fulfillmentText": response_text
        })
    else:
        return HttpResponse()


def opcoes_intent(req) -> str:
    intent_name = req.get('queryResult').get('intent').get('displayName')

    if intent_name == 'Default Welcome Intent':
        response_text = """Olá! Seja bem-vindo(a)! Eu sou o Ravis(Assistente virtual da DreamStore)
                Deseja iniciar o atendimento?
                1️⃣Sim
                2️⃣Não"""
    elif intent_name == 'resposta-sim':
        response_text = """Para agilizar o atendimento. Por favor, escolha uma das opções abaixo:
                1️⃣Lista de produtos
                2️⃣Itens comprados
                3️⃣Falar com atendente
                4️⃣Encerrar Atendimento
            """
    elif intent_name == 'respostaNao':
        response_text = """Ok. Precisando, estamos a disposição para melhor atendê-lo!
        Querendo retornar ao menu de opções digite: MENU. Bye, Bye!"""
    elif intent_name == 'ListarProdutos':
        products = Product.objects.all()
        lista_products = [f"{product.name} - R$ {product.price}- Quant.: {product.stock}" for product in products]
        response_text = "Aqui está a lista de produtos:\n" + "\n".join(lista_products)
    elif intent_name == 'BuscarProduto':
        parameters = req.get('queryResult').get('parameters')
        name = parameters.get('name')
        try:
            product = Product.objects.get(name__icontains=name)
            response_text = f"ID..: {product.id} - {product.name} - R$ {product.price}- Quant.: {product.stock}"
        except Product.DoesNotExist:
            response_text = "Desculpe, produto não existe em nossa loja!"
        return response_text
    elif intent_name == 'CadastrarProduto':
        parameters = req.get('queryResult').get('parameters')
        name = parameters.get('name')
        price = parameters.get('price')
        stock = parameters.get('stock')
        payload = {
            'name': name,
            'price': price,
            'stock': stock
        }
        product = Product.objects.create(**payload)
        response_text = f"Produto: {product.name} - R$ {product.price} - Quantidade: {product.stock}"
    elif intent_name == 'AtualizarProduto':
        parameters = req.get('queryResult').get('parameters')
        old_name = parameters.get('old_name')[0]
        new_name = parameters.get('new_name')[0]
        try:
            product = Product.objects.get(name__icontains=old_name[0])
            product.price
            product.stock
            payload = {
                'name': new_name,
                'price': price,
                'stock': stock
            }
            p = Product.objects.update_or_create(**payload)
            response_text = (f"ID..: {p.id} - {p.name} - R$ {p.price}- Quant.: {p.stock}"
                             f" atualizado com sucesso!")
        except Product.DoesNotExist:
            response_text = "Desculpe, produto não existe em nossa loja!"
        return response_text
    else:
        response_text = "Intenção não reconhecida"

    return response_text



# def dialogflow_webhook(request):
#     if request.method == 'POST':
#         req = json.loads(request.body)
#
#         # Extraia a intenção e parâmetros
#         intent_name = req.get('queryResult').get('intent').get('displayName')
#
#         # Lógica personalizada para cada intenção
#         if intent_name == 'SuaIntencaoEspecifica':
#             response_text = "Resposta personalizada para a intenção"
#         else:
#             response_text = "Intenção não reconhecida"
#
#         # Responder ao Dialogflow com fulfillmentMessages
#         return JsonResponse({
#             "fulfillmentMessages": [
#                 {
#                     "text": {
#                         "text": [response_text]
#                     }
#                 }
#             ]
#         })
