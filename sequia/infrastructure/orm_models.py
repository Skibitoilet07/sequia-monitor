from django.db import models

class Region(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        app_label = 'sequia'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class FuenteHidrica(models.Model):
    TIPO_CHOICES = [
        ("REUSO", "Reúso de aguas tratadas"),
        ("DESALACION", "Desalación modular"),
        ("RECARGA", "Recarga de acuíferos"),
        ("TELEMETRIA", "Telemetría y control de extracciones"),
        ("OTRA", "Otra solución"),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    capacidad_m3d = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    energia_renovable = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True)

    class Meta:
        app_label = 'sequia'

    def __str__(self):
        return self.get_tipo_display()


class Medida(models.Model):
    nombre = models.CharField(max_length=150)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    fuente = models.ForeignKey(FuenteHidrica, on_delete=models.SET_NULL, null=True, blank=True)
    objetivo = models.TextField()
    avance_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)

    class Meta:
        app_label = 'sequia'

    def __str__(self):
        return self.nombre


class Indicador(models.Model):
    medida = models.ForeignKey(Medida, on_delete=models.CASCADE, related_name="indicadores")
    fecha = models.DateField()
    volumen_reutilizado_m3d = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    perdidas_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    nivel_freatico_m = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    caudal_ecologico_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        app_label = 'sequia'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.medida.nombre} - {self.fecha}"
