from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User


class Categories(models.Model):
    title = models.CharField(max_length=80)


class CategoryEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Categories):
            return {"id": obj.id, "title": obj.title}
        return super().default(obj)


class Cards(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=6000, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)


class CardEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Cards):
            return {"id": obj.id, "title": obj.title}
        return super().default(obj)


class CardVariants(models.Model):
    title = models.CharField(max_length=200)
    quantity = models.IntegerField()
    cost = models.FloatField()
    card = models.ForeignKey(Cards, on_delete=models.CASCADE, null=True)


class CardVariantEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, CardVariants):
            return {
                "id": obj.id,
                "title": obj.title,
                "quantity": obj.quantity,
                "cost": obj.cost,
            }
        return super().default(obj)


class CardImages(models.Model):
    path = models.CharField(max_length=400)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"path: {self.path} card: {self.card.id}"


class CardImageEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, CardImages):
            return {
                "id": obj.id,
                "title": obj.title,
            }
        return super().default(obj)


class Filters(models.Model):
    is_choice = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)


class FilterValues(models.Model):
    answer = models.CharField(max_length=100)
    filters = models.ForeignKey(Filters, on_delete=models.CASCADE, null=True)
    card = models.ForeignKey(Cards, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return (
            f"answer: {self.answer}, filters: {self.filters.id}, card: {self.card.id}"
        )


class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    fio = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    house = models.CharField(max_length=10)
    corps = models.CharField(max_length=10, null=True)
    flat = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=20)


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    is_delivery = models.BooleanField()
    status = models.CharField(max_length=100)
    comment = models.CharField(max_length=300)
    track = models.CharField(max_length=50, null=True)

    fio = models.CharField(max_length=200)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=30)
    corps = models.CharField(max_length=30)
    room = models.CharField(max_length=30)
    phone = models.CharField(max_length=50)


class OrderEntries(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True)

    variant = models.ForeignKey(CardVariants, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    buy_cost = models.FloatField()


class Works(models.Model):
    title = models.CharField(max_length=200)


class WorkImages(models.Model):
    path = models.CharField(max_length=300)
    work = models.ForeignKey(Works, on_delete=models.CASCADE, null=True)


class Certificates(models.Model):
    title = models.CharField(max_length=200)


class CertificateImages(models.Model):
    path = models.CharField(max_length=300)
    certificate = models.ForeignKey(Certificates, on_delete=models.CASCADE, null=True)
