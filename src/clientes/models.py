from django.db import models
import uuid
from django.utils.text import slugify

# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    cpf  = models.CharField(max_length=14, null=True, blank=True)
    ddd = models.CharField(max_length=2, null=True, blank=True)
    telefone = models.CharField(max_length=9, null=True, blank=True)
    criadoem = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)


    class Meta:
        ordering = ('-criadoem',)

    def __str__(self) -> str:
        return str(self.nome)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug from 'nome' field if slug is not provided
            self.slug = slugify(self.nome)

            # Check if the generated slug already exists, append count if necessary
            slug_base = self.slug
            count = 1
            while Cliente.objects.filter(slug=self.slug).exists():
                self.slug = f'{slug_base}-{count}'
                count += 1

        super().save(*args, **kwargs)