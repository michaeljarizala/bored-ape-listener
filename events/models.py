from django.db import models

class Transfer(models.Model):
    token_id = models.CharField(max_length=42)
    sender = models.CharField(max_length=42)
    recipient = models.CharField(max_length=42)
    trn_hash = models.CharField(max_length=64, unique=True)
    block_no = models.IntegerField()