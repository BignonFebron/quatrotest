from django.db import models

class APIKeys(models.Model):
  user_id=models.IntegerField(null=False)
  created_at=models.DateTimeField(auto_now_add=True)
  public_key=models.CharField(max_length=64)
  private_key=models.CharField(max_length=64)