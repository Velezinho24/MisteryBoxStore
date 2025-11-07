"""
Servicios para Mystery Boxes
"""
import random
from decimal import Decimal


def select_random_product_weighted(mystery_box):
    """
    Selecciona un producto aleatorio de la mystery box con ponderación.
    Los productos más BARATOS tienen MAYOR probabilidad de salir.
    
    Estrategia: peso = max_price - product_price + 1
    Esto hace que productos baratos tengan pesos altos.
    
    Args:
        mystery_box: instancia de MysteryBox
        
    Returns:
        Product: el producto seleccionado aleatoriamente
        
    Raises:
        ValueError: si la caja no tiene productos
    """
    products = list(mystery_box.products.all())
    
    if not products:
        raise ValueError(f"Mystery box '{mystery_box.name}' no tiene productos")
    
    # Si solo hay un producto, retornarlo directamente
    if len(products) == 1:
        return products[0]
    
    # Obtener precio máximo de la caja
    max_price = max(p.price_cop for p in products)
    
    # Calcular pesos: productos baratos tienen mayor peso
    # Fórmula: peso = (max_price - precio_producto) + base
    # El +1 asegura que incluso el producto más caro tenga algo de probabilidad
    base_weight = max_price * Decimal('0.1')  # 10% del precio máximo como base
    
    weights = []
    for product in products:
        # Peso inverso al precio
        weight = float(max_price - product.price_cop + base_weight)
        weights.append(weight)
    
    # Seleccionar usando random.choices con pesos
    selected = random.choices(products, weights=weights, k=1)[0]
    
    return selected


def calculate_mystery_box_stats(mystery_box):
    """
    Calcula estadísticas de probabilidad para una mystery box.
    
    Returns:
        dict con:
            - total_products: número total de productos
            - product_probabilities: lista de (product, probability_percent)
            - avg_value: valor promedio esperado
            - min_value: valor mínimo
            - max_value: valor máximo
    """
    products = list(mystery_box.products.all())
    
    if not products:
        return {
            'total_products': 0,
            'product_probabilities': [],
            'avg_value': 0,
            'min_value': 0,
            'max_value': 0
        }
    
    max_price = max(p.price_cop for p in products)
    base_weight = max_price * Decimal('0.1')
    
    # Calcular pesos totales
    total_weight = 0
    product_weights = []
    
    for product in products:
        weight = float(max_price - product.price_cop + base_weight)
        product_weights.append((product, weight))
        total_weight += weight
    
    # Calcular probabilidades en porcentaje
    product_probabilities = []
    expected_value = 0
    
    for product, weight in product_weights:
        probability = (weight / total_weight) * 100
        product_probabilities.append({
            'product': product,
            'probability': round(probability, 2),
            'weight': weight
        })
        expected_value += float(product.price_cop) * (weight / total_weight)
    
    # Ordenar por probabilidad descendente
    product_probabilities.sort(key=lambda x: x['probability'], reverse=True)
    
    return {
        'total_products': len(products),
        'product_probabilities': product_probabilities,
        'avg_value': round(expected_value, 2),
        'min_value': min(p.price_cop for p in products),
        'max_value': max(p.price_cop for p in products),
    }
