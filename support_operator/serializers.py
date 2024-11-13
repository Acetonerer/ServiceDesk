from rest_framework import serializers
from support_operator.models import SupportOperator


class SupportOperatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportOperator
        fields = ["operator_id", "operator_name"]
