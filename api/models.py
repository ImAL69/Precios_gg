from django.db import models

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre_categoria

class Juego(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha_lanzamiento = models.DateField(blank=True, null=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='juegos')

    def __str__(self):
        return self.titulo

class Plataforma(models.Model):
    nombre_plataforma = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre_plataforma

class Precio(models.Model):
    id_juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='precios')
    id_plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE, related_name='precios')
    precio_actual = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=10, default='COP')
    fecha_consulta = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_juego.titulo} en {self.id_plataforma.nombre_plataforma}: {self.precio_actual} {self.moneda}"
