import json

from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

from .models import Product


@csrf_exempt
def webhook(request: HttpRequest) -> HttpResponse:
    """Handle webhook requests from Dialogflow."""
    if request.method == 'POST':
        req = json.loads(request.body)

        response_text = opcoes_intent(req)

        return JsonResponse({
            "fulfillmentText": response_text,
            "outputContexts": [
                {
                    "name": f"{req.get('session')}/contexts/awaiting_product_choice",
                    "lifespanCount": 5
                }
            ]
        })
    else:
        return HttpResponse()


def opcoes_intent(req) -> str:
    intent_name = req.get('queryResult').get('intent').get('displayName')
    print(intent_name)

    if intent_name == 'Default Welcome Intent':
        response_text = """Olá! Seja bem-vindo(a)! Eu sou o Ravis(Assistente virtual da DreamStore)
               Deseja iniciar o atendimento?
               - SIM
               - NÃO"""
    # elif intent_name == 'respostaNao':
    #     response_text = """Ok. Precisando, estamos a disposição para melhor atendê-lo!Bye, Bye!
    # """
    elif intent_name == 'answerNo':
        response_text = """Pôxa que pena...
        
        Siga-nos nas nossas redes sociais:
        
        @instagram
        @facebook
        @X (antigo Twitter)
        
        Para finalizar, digite SAIR!        
        """
    elif intent_name == 'answerYes':
        total_length = 30
        fill_char = "="
        name = req.get('queryResult').get('parameters').get('name')
        products = Product.objects.all()
        first_string = f"""Ok. {name}. 
        Escolha o produto:
        """
        response = first_string
        for product in products:
            response += f"""
            {product.name.center(total_length, fill_char).upper()}
            """
        response_text = response
    elif intent_name == 'productChoice':
        product = req.get('queryResult').get('parameters').get('product')
        response_text = f'Voce escolheu o {product}. Posso confirmar?'
    elif intent_name == 'productCancel':
        response_text = '''Que pena.
        Para voltar ao menu Principal. Digite VOLTAR.
        Para sair do atendimento. Digite SAIR.
        '''
    elif intent_name == 'productConfirmYes':
        name = req['queryResult']['outputContexts'][0].get('parameters')['name']
        product = req['queryResult']['outputContexts'][0].get('parameters')['product']
        response_text = f'''Ótimo sr(a). {name}. Produto {product} adicionado com sucesso!
        Para voltar ao menu Principal. Digite VOLTAR.
        Para sair do atendimento. Digite SAIR.
        '''
    # elif intent_name == 'BuscarProduto':
    #     parameters = req.get('queryResult').get('parameters')
    #     name = parameters.get('name')
    #     try:
    #         product = Product.objects.get(name__icontains=name)
    #         response_text = f"ID..: {product.id} - {product.name} - R$ {product.price}- Quant.: {product.stock}"
    #     except Product.DoesNotExist:
    #         response_text = "Desculpe, produto não existe em nossa loja!"
    # elif intent_name == 'Comprar':
    #     products = Product.objects.all()
    #     list_products = []
    #     for product in products:
    #         str_product = "-".join((str(product.id), product.name))
    #         list_products.append(str_product)
    #     response_text = f"Temos os produtos: {list_products}. Por favor, escolha qual desses quer comprar:"
    # elif intent_name == "EscolhaDoProduto":
    #     requisition = req.get('queryResult').get('parameters')
    #     product_number = requisition.get('product_number')
    #     p = req.get('queryResult').get('parameters', {}).get('product_number')
    #     try:
    #         product = Product.objects.get(id=product_number)
    #         response_text = f"ID..: {product.id} - {product.name} - R$ {product.price}- Quant.: {product.stock}"
    #     except Product.DoesNotExist:
    #         response_text = "Desculpe, produto não existe em nossa loja!"
    elif intent_name == 'dreamStoreExit':
        response_text = 'Muito obrigado interagir comigo, até mais!'
    else:
        response_text = "Intenção não reconhecida"

    return response_text
