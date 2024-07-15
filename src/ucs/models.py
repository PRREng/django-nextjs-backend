from django.db import models
from clientes.models import Cliente
import num2words

# Create your models here.
class Endereco(models.Model):

    PREFIXO_LOCAL_CHOICES = [
        ('Rua', 'Rua'),
        ('Av.', 'Avenida'),
        ('Pov.', 'Povoado'),
        ('Est.', 'Estrada'),
        # Add more choices as needed
    ]

    ESTADO_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ]


    CEP = models.CharField(max_length=9) #49045-080
    prefixo_local = models.CharField(max_length=4, choices=PREFIXO_LOCAL_CHOICES)
    rua = models.CharField(max_length=200)
    num_logradouro = models.CharField(max_length=5)
    bairro = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES)
    seforrural = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.prefixo_local} {self.rua}, {self.num_logradouro} - {self.bairro}, {self.cidade} - {self.estado}"
    
    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def getCep(self) -> str:
        return self.CEP[:5] + '-' + self.CEP[5:]


    def getEndereco(self) -> str:
        return f"{self.prefixo_local} {self.rua}, {self.num_logradouro} - {self.bairro}, {self.cidade} - {self.estado}"


class Categoria(models.Model):
    nomeCategoria = models.CharField(max_length=10, choices=[
        ('Monofásico', 'Monofásico'), ('Bifásico', 'Bifásico'), ('Trifásico', 'Trifásico')])

    def __str__(self):
        return f"{self.nomeCategoria}"


class TipoUC(models.Model):
    nomeTipo = models.CharField(max_length=12, choices=[('Usina', 'Usina'), ('Compensadora', 'Compensadora')])

    def __str__(self):
        return f"{self.nomeTipo}"


class UC(models.Model):

    tensaoNominalCHOICES = [
        ('127/220', '127/220'),
        ('220/380', '220/380')
        # Add more choices as needed
    ]

    residenceoucomerceCHOICES = [
        ('Residencial', 'Residencial'),
        ('Comercial', 'Comercial')
        # Add more choices as needed
    ]

    num_UC = models.CharField(max_length=50)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ucs')
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    tipoUC = models.ForeignKey(TipoUC, on_delete=models.CASCADE)
    consumo = models.DecimalField(max_digits=10, decimal_places=2)
    tempoPosse = models.IntegerField(default=0)
    tensaoNominal = models.CharField(max_length=10, choices=tensaoNominalCHOICES)
    resideoucomercial = models.CharField(max_length=11, choices=residenceoucomerceCHOICES)

    class Meta:
        ordering = ('tipoUC',)
    
    def __str__(self):
        return f"UC {self.num_UC} - Proprietário: {self.cliente.nome}"
    

    def getAnoExtenso(self) -> str:
        numero_ext = num2words.num2words(self.tempoPosse, lang='pt-br').upper()
        return numero_ext
    
class ModuloSolar(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    potencia = models.DecimalField(max_digits=6, decimal_places=2)
    area = models.DecimalField(max_digits=4, decimal_places=2)
    peso = models.DecimalField(max_digits=4, decimal_places=2)
    garantiaAno = models.IntegerField()
    codInmetro = models.CharField(max_length=12)

    def __str__(self):
        return f"Módulo Solar Marca: {self.marca} Modelo: {self.modelo} Potencia: {self.potencia} Wp"
    

class Projeto(models.Model):
    uc = models.ForeignKey(UC, on_delete=models.CASCADE)
    modulo = models.ForeignKey(ModuloSolar, on_delete=models.CASCADE)
    consumoTotal = models.IntegerField()
    qtdeModulos = models.IntegerField()
    producaoMedia = models.DecimalField(max_digits=10, decimal_places=2)
    qtdeInv = models.IntegerField()
    valorProposta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Projeto da UC: {self.uc.num_UC} no nome do cliente {self.uc.cliente.nome} com consumo de {self.consumoTotal} kwh"
    
    def isPlural(self):
        return self.qtdeInv > 1