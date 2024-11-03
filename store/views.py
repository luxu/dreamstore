import json

from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from dialogflow_fulfillment import QuickReplies, WebhookClient

from logging import getLogger

from . import serializers
from .models import Product

logger = getLogger('django.server.webhook')

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


# Define a custom handler function
def handler(agent: WebhookClient) -> None:
    """
    This handler sends a text message along with a quick replies message
    back to Dialogflow, which uses the messages to build the final response
    to the user.
    """

@csrf_exempt
def webhook(request: HttpRequest) -> HttpResponse:
    """Handle webhook requests from Dialogflow."""
    if request.method == 'POST':
        # Get WebhookRequest object
        request_ = json.loads(request.body)

        # Log request headers and body
        logger.info(f'Request headers: {dict(request.headers)}')
        logger.info(f'Request body: {request_}')

        # Handle request
        agent = WebhookClient(request_)
        agent.handle_request(handler)

        # Log WebhookResponse object
        logger.info(f'Response body: {agent.response}')

        return JsonResponse(agent.response)

    return HttpResponse()


def dialogflow_webhook(request):
    if request.method == 'POST':
        req = json.loads(request.body)

        # Extraia a intenção e parâmetros
        intent_name = req.get('queryResult').get('intent').get('displayName')
        parameters = req.get('queryResult').get('parameters')

        # Exemplo de resposta
        if intent_name == 'Welcome':
            response_text = "Resposta personalizada baseada na intenção"
        else:
            response_text = "Intenção não reconhecida"

        return JsonResponse({
            "fulfillmentText": response_text
        })
    else:
        return HttpResponse()
