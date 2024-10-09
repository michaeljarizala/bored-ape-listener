from rest_framework import serializers
from events.models import Transfer

class TransferSerializer(serializers.ModelSerializer):
    token_id=serializers.CharField(max_length=42)
    sender=serializers.CharField(max_length=42)
    recipient=serializers.CharField(max_length=42)
    trn_hash=serializers.CharField(max_length=64)
    block_no=serializers.IntegerField()

    class Meta:
        model = Transfer
        fields = [
            'id',
            'token_id',
            'sender',
            'recipient',
            'trn_hash',
            'block_no',
        ]

