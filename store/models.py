from django.db import models


class Product(models.Model):
    name = models.CharField(
        'Nome do Produto',
        max_length=100
    )
    price = models.DecimalField(
        'Valor do Produto',
        max_digits=10, decimal_places=2
    )
    stock = models.IntegerField(
        'Quantidade em estoque',
        default=0
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
