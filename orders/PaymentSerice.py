import stripe
from django.conf import settings
from . models import Orders
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentService:
    @staticmethod
    def create_checkout_session(order):
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'Order {order.number}'
                    },
                    'unit_amount': int(order.total_price * 100),
                },
                'quantity': 1,
            }],
            model='payment',
            success_url=settings.STRIPE_SUCCESS_URL, #STRIPE_SUCCESS_URL ?
            cansel_url=settings.STRIPE_CANSEL_URL,
        )
        return session.id


class StripeWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET # нужно не забыть добавить
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            order_id = session['metadata']['order_id']
            Orders.objects.filter(id=order_id).update(status='paid')

        return Response({'status': 'success'}, status=status.HTTP_200_OK)



# import stripe
# from django.conf import settings
# from .models import Orders
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
#
# stripe.api_key = settings.STRIPE_SECRET_KEY
#
# class PaymentService:
#     @staticmethod
#     def create_checkout_session(order):
#         session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[{
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': f'Order {order.number}'
#                     },
#                     'unit_amount': int(order.total_price * 100),  # Сумма в центах
#                 },
#                 'quantity': 1,
#             }],
#             mode='payment',
#             success_url=settings.STRIPE_SUCCESS_URL + f"?session_id={{CHECKOUT_SESSION_ID}}",
#             cancel_url=settings.STRIPE_CANCEL_URL,
#             metadata={
#                 'order_id': str(order.id)
#             }
#         )
#         return session.id
#
# class StripeWebhookView(APIView):
#     def post(self, request, *args, **kwargs):
#         payload = request.body
#         sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#         endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
#         event = None
#
#         try:
#             event = stripe.Webhook.construct_event(
#                 payload, sig_header, endpoint_secret
#             )
#         except ValueError as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#         if event['type'] == 'checkout.session.completed':
#             session = event['data']['object']
#             order_id = session['metadata']['order_id']
#             Orders.objects.filter(id=order_id).update(status='paid')
#
#         return Response({'status': 'success'}, status=status.HTTP_200_OK)