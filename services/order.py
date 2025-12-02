from typing import List, Optional
from django.db import transaction
from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: Optional[str] = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )

    return order


def get_orders(username: Optional[str] = None) -> List[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
