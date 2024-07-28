from django.shortcuts import render

# Create your views here.
class Record(models.Model):
    RECORD_TYPES = (
        ('completed', 'Completed Order'),
        ('deduction', 'Order Deduction'),
    )
    
    title = models.CharField(max_length=100)
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES)
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f"{self.title} - {self.date}"
    
def records_view(request):
    return render(request, 'accounts/records.html')