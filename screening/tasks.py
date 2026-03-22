from celery import shared_task
from django.utils import timezone
from .models import SeatReservation


@shared_task
def release_expired_reservations():
    expired = SeatReservation.objects.filter(
        status=SeatReservation.Status.RESERVED,
        expires_at__lt=timezone.now()
    )
    count = expired.count()
    expired.update(
        status=SeatReservation.Status.AVAILABLE,
        user=None,
        expires_at=None
    )
    return f'{count} reservas expiradas liberadas'


@shared_task
def send_ticket_confirmation(ticket_id):
    from .models import Ticket
    ticket = Ticket.objects.get(id=ticket_id)
    # aqui entraria o envio de email
    return f'Confirmação enviada para {ticket.user.email}'