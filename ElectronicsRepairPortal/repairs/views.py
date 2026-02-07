
from django.shortcuts import render, redirect, get_object_or_404
from .models import RepairTicket, Customer, TicketUpdate, Estimate, Schedule
from .forms import CustomerForm, ItemDescriptionForm, RepairTicketForm, EstimateForm
import random

def base(request):
        return render(request, "repairs/base.html")

def ticket_list(request):
    tickets = RepairTicket.objects.all().order_by('-created_at')
    return render(request, "repairs/ticket_list.html", {"tickets": tickets})

def generate_unique_ticket_number():
	while True:
		number = f'{random.randint(0,999999):06d}'
		if not RepairTicket.objects.filter(ticket_number=number).exists():
			return number

def ticket_create(request):
	if request.method == "POST":
		customer_form = CustomerForm(request.POST)
		item_form = ItemDescriptionForm(request.POST)
		ticket_form = RepairTicketForm(request.POST)
		if customer_form.is_valid() and ticket_form.is_valid() and item_form.is_valid():
			customer, _ = Customer.objects.get_or_create(
			first_name=customer_form.cleaned_data['first_name'],
			last_name=customer_form.cleaned_data['last_name'],
			phone=customer_form.cleaned_data['phone'],
			email=customer_form.cleaned_data.get('email'),
			address=customer_form.cleaned_data.get('address'),
			city=customer_form.cleaned_data.get('city'),
			zip_code=customer_form.cleaned_data.get('zip_code'),
		)
		item = item_form.save()
		ticket = ticket_form.save(commit=False)
		ticket.customer = customer
		ticket.item_description = item
		ticket.ticket_number = generate_unique_ticket_number()
		ticket.warranty = ticket_form.cleaned_data.get('warranty')
		ticket.save()
		return redirect("ticket_detail", pk=ticket.pk)
	else:
		customer_form = CustomerForm()
		item_form = ItemDescriptionForm()
		ticket_form = RepairTicketForm()
	return render(request, "repairs/ticket_form.html", {
		"customer_form": customer_form,
		"item_form": item_form,
		"ticket_form": ticket_form,
	})

def ticket_detail(request, pk):
    ticket = get_object_or_404(RepairTicket, pk=pk)
    updates = TicketUpdate.objects.filter(ticket=ticket)
    estimate = Estimate.objects.filter(ticket=ticket).last()
    schedule = Schedule.objects.filter(ticket=ticket).last()
    return render(request, "repairs/ticket_detail.html", {
        "ticket": ticket,
        "updates": updates,
        "estimate": estimate,
        "schedule": schedule,
    })

# Update Ticket (Tech only)
def ticket_update(request, pk):
    ticket = get_object_or_404(RepairTicket, pk=pk)
    if request.method == "POST":
        form = TicketUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.ticket = ticket
            update.save()
            return redirect("ticket_detail", pk=pk)
    else:
        form = TicketUpdateForm()
    return render(request, "repairs/update_ticket.html", {"form": form, "ticket": ticket})

# Create Estimate
def estimate_create(request, pk):
    ticket = get_object_or_404(RepairTicket, pk=pk)
    if request.method == "POST":
        form = EstimateForm(request.POST)
        if form.is_valid():
            estimate = form.save(commit=False)
            estimate.ticket = ticket
            estimate.save()
            return redirect("ticket_detail", pk=pk)
    else:
        form = EstimateForm()
    return render(request, "repairs/estimate_form.html", {"form": form, "ticket": ticket})

# Create Schedule
def schedule_create(request, pk):
    ticket = get_object_or_404(RepairTicket, pk=pk)
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.ticket = ticket
            schedule.save()
            return redirect("ticket_detail", pk=pk)
    else:
        form = ScheduleForm()
    return render(request, "repairs/schedule_form.html", {"form": form, "ticket": ticket})
