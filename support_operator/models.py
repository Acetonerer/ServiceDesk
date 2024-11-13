from django.db import models


class SupportOperator(models.Model):
    operator_id = models.IntegerField(primary_key=True)
    operator_name = models.CharField(max_length=30)

    class Meta:
        ordering = ['operator_id']
        db_table = 'support_operator'

    def __str__(self):
        return f"{self.operator_name}"
