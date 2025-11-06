#!/usr/bin/env python
"""
Script de prueba para verificar el sistema de selección aleatoria de Mystery Boxes
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MisteryBoxStore.settings")
django.setup()

from mistery_boxes.models import MysteryBox
from mistery_boxes.services import select_random_product_weighted, calculate_mystery_box_stats

def test_selection():
    boxes = MysteryBox.objects.filter(is_active=True).prefetch_related('products')
    
    if not boxes.exists():
        print("❌ No hay mystery boxes activas")
        return
    
    for box in boxes:
        print(f"\n{'='*60}")
        print(f"🎁 Mystery Box: {box.name}")
        print(f"💰 Precio: ${box.price_cop:,}")
        print(f"📦 Productos: {box.products.count()}")
        print(f"{'='*60}\n")
        
        # Calcular estadísticas
        stats = calculate_mystery_box_stats(box)
        
        print(f"📊 Estadísticas:")
        print(f"   - Valor mínimo: ${stats['min_value']:,}")
        print(f"   - Valor promedio: ${stats['avg_value']:,}")
        print(f"   - Valor máximo: ${stats['max_value']:,}")
        print(f"\n🎲 Probabilidades:")
        
        for prob_data in stats['product_probabilities']:
            product = prob_data['product']
            probability = prob_data['probability']
            print(f"   - {product.name[:40]:40} ${product.price_cop:>8,} ({probability:>6.2f}%)")
        
        # Hacer 100 selecciones de prueba
        print(f"\n🧪 Simulación (100 selecciones):")
        selections = {}
        
        for _ in range(100):
            selected = select_random_product_weighted(box)
            selections[selected.id] = selections.get(selected.id, 0) + 1
        
        # Mostrar resultados
        for product_id, count in sorted(selections.items(), key=lambda x: x[1], reverse=True):
            product = box.products.get(id=product_id)
            print(f"   - {product.name[:40]:40} {count:>3} veces ({count}%)")
        
        print()

if __name__ == "__main__":
    test_selection()
