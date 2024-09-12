import math

from utils import formatDateAndHour

def findTimestamp(history, status):
    # Encontra o timestamp para um status específico ou retorna None se não encontrado
    result = next((i for i in history if i['status'] == status), None)
    return formatDateAndHour(result['timestamp']) if result else None

def getOrderDates(order):
    # Use a função findTimestamp para buscar e formatar as datas
    return {
        "preparation_start_datetime": findTimestamp(order['history'], 'PREPARING'),
        "prepared_datetime": findTimestamp(order['history'], 'PREPARED'),
        "assigned_datetime": findTimestamp(order['history'], 'ASSIGNED'),
        "collected_datetime": findTimestamp(order['history'], 'COLLECTED'),
        "datetime_finished": findTimestamp(order['history'], 'COMPLETED')
    }

def getRelevantAddress(address):
    return {
        "street": address['street'],
        "neighborhood": address['neighborhood'],
        "city": address['city'],
        "state": address['state']
    }


def getOrderPaymentDetailsAndOrderFee(order):
    # Verifica se 'paymentExtraInfo' está presente e não é None
    if order and 'paymentExtraInfo' in order and order['paymentExtraInfo']:
        payment_extra_info = order['paymentExtraInfo']
        discount_coupons = payment_extra_info.get('discountCoupons', [])
    else:
        discount_coupons = []

    # Calcula os descontos
    discounts = sum(float(coupon['value']) for coupon in discount_coupons)
    discounts = discounts if discounts else 0

    # Verifica se 'ifoodOrder' e 'total' estão presentes e não são None
    if order and 'ifoodOrder' in order and order['ifoodOrder'] and 'total' in order['ifoodOrder'] and order['ifoodOrder']['total']:
        additional_fees = order['ifoodOrder']['total'].get('additionalFees', 0)
    else:
        additional_fees = 0

    # Calcula o subtotal
    sub_total = order['amount'] - additional_fees - \
        order['deliveryFee'] + discounts

    return {
        "additional_fee": additional_fees,
        "deliveryman_fee": order['deliverymanFee'],
        "delivery_fee": order['deliveryFee'],
        "payment_type": payment_type_map[order['paymentType']](),
        "prepaid": order['isPrepaid'],
        "discounts": discounts,
        "subtotal": sub_total,
        "total": order['amount']
    }


# Mapeamento de tipos de pagamento para suas respectivas funções
payment_type_map = {
    'CASH': lambda: 'Dinheiro',
    'PIX': lambda: 'Pix',
    'CREDIT': lambda: 'Cartão de Crédito',
    'DEBIT': lambda: 'Cartão de Débito',
    'DIGITAL_WALLET': lambda: 'Carteira Digital',
    'GIFT_CARD': lambda: 'Gift Card',
    'FOOD_VOUCHER': lambda: 'Vale Alimentação',
    'MEAL_VOUCHER': lambda: 'Vale Refeição',
    'OTHER': lambda: 'Outro',
}
