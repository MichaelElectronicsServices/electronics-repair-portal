from django.db import models
from django.utils import timezone


# Create your models here.from django.db import mode
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"

class Item_description(models.Model):
    brand = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    issue_description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RepairTicket(models.Model):
    STATUS_CHOICES = [
                ("new", "New"),
                ("diagnosing", "Diagnosing"),
                ("estimate_sent", "Estimate Sent"),
                ("awaiting_approval", "Awaiting Approval"),
                ("scheduled", "Scheduled"),
                ("in_repair", "In Repair"),
                ("completed", "Completed"),
                ("cancelled", "Cancelled"),

    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tickets')
    item_description = models.ForeignKey(Item_description, on_delete=models.CASCADE, related_name='tickets')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    ticket_number = models.CharField(max_length=6, unique=True, editable=False)
    warranty = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"Ticket #{self.ticket_number} - {self.customer}"

class TicketUpdate(models.Model):
    ticket = models.ForeignKey(
                RepairTicket,
                on_delete=models.CASCADE,
                related_name="updates"

    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    internal_only = models.BooleanField(
                    default=False,
                    help_text="Visible only to technicians"

            )

def __str__(self):
    return f"Update for Ticket #{self.ticket.id}"

class Estimate(models.Model):
    ticket = models.ForeignKey(
        RepairTicket,
        on_delete=models.CASCADE,
        related_name="estimates"
    )

    labor_total = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        help_text="labor cost"
    )

    parts_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    notes = models.TextField(blank=True)

    approved = models.BooleanField(null=True)
    # None = pending, True = approved, False = rejected

    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def total_cost(self):
        return self.labor_total + self.parts_cost

    def __str__(self):
        return f"Estimate for Ticket #{self.ticket.id} - ${self.total_cost}"


class Part(models.Model):
    ticket = models.ForeignKey(RepairTicket, on_delete=models.CASCADE, related_name='parts')
    part_number = models.CharField(max_length=100)
    part_description = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} for {self.ticket.ticket_number}"
class Schedule(models.Model):
    ticket = models.ForeignKey(
        RepairTicket,
        on_delete=models.CASCADE,
        related_name="schedules"
    )

    scheduled_for = models.DateTimeField()
    confirmed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Schedule for Ticket #{self.ticket.id}"

