from my_app.models import MenuItem, Order, OrderItem
from my_app.utilities import compute_order_total 

def test_compute_order_total(db_session):
    menu_item1 = MenuItem(name="Burger", price=8.0)
    menu_item2 = MenuItem(name="Fries", price=4.0)
    db_session.add_all([menu_item1, menu_item2])
    db_session.commit()

    order = Order(total = 0.0)
    db_session.add(order)
    db_session.commit()

    order_item1 = OrderItem(order_id=order.id, menu_item_id=menu_item1.id, quantity=2)
    order_item2 = OrderItem(order_id=order.id, menu_item_id=menu_item2.id, quantity=3)
    db_session.add_all([order_item1, order_item2])
    db_session.commit()

    total = compute_order_total(order, db_session)
    assert total == 8.0 * 2 + 4.0 * 3