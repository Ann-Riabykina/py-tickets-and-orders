from django.db import transaction
from db.models import Order, Ticket, User


@transaction.atomic
def create_order(tickets: list, username: str, date=None):
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for t in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=t["movie_session"],
            row=t["row"],
            seat=t["seat"]
        )

    return order


def get_orders(username=None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()