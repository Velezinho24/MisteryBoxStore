# Generated migration to add slug field to Product model

from django.db import migrations, models
from django.utils.text import slugify


def generate_slugs(apps, schema_editor):
    """Generate unique slugs for all existing products"""
    Product = apps.get_model('catalog', 'Product')
    
    for product in Product.objects.all():
        base_slug = slugify(product.name)
        slug = base_slug
        counter = 1
        
        # Ensure uniqueness
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        product.slug = slug
        product.save()


def reverse_slugs(apps, schema_editor):
    """No need to reverse - slugs will be deleted with the field"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_product_image'),
    ]

    operations = [
        # Step 1: Add slug field without unique constraint, allowing blank
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, default=''),
        ),
        # Step 2: Populate slugs for existing products
        migrations.RunPython(generate_slugs, reverse_slugs),
        # Step 3: Make slug field unique and non-blank
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
