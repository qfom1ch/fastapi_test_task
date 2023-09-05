from sqladmin import ModelView

from apps.customer.models import Customer
from apps.order.models import Order
from apps.store.models import Store
from apps.visit.models import Visit
from apps.worker.models import Worker


class WorkerAdmin(ModelView, model=Worker):
    column_list = [Worker.id, Worker.name, Worker.phone, Worker.stores]
    column_searchable_list = [Worker.id, Worker.name, Worker.phone]
    column_sortable_list = [Worker.id, Worker.name]
    name = "Работник"
    name_plural = "Работники"
    icon = "fa-solid fa-user"


class StoreAdmin(ModelView, model=Store):
    column_list = [Store.id, Store.name, Store.workers]
    column_searchable_list = [Store.id, Store.name]
    column_sortable_list = [Store.id, Store.name]
    name = "Магазин"
    name_plural = "Магазины"
    icon = "fa-solid fa-store"


class CustomerAdmin(ModelView, model=Customer):
    column_list = [Customer.id, Customer.name, Customer.phone,
                   Customer.store]
    column_searchable_list = [Customer.id, Customer.name, Customer.phone]
    column_sortable_list = [Customer.id, Customer.name]
    name = "Заказчик"
    name_plural = "Заказчики"
    icon = "fa-solid fa-user"


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.status, Order.creation_time, Order.end_time,
                   Order.worker, Order.store, Order.customer]
    column_searchable_list = [Order.id, Order.status]
    column_sortable_list = [Order.id, Order.status, Order.creation_time,
                            Order.end_time]
    name = "Заказ"
    name_plural = "Заказы"
    icon = "fa-solid fa-cart-shopping"


class VisitAdmin(ModelView, model=Visit):
    column_list = [Visit.creation_time, Visit.customer,
                   Visit.order, Visit.worker, Visit.store]
    column_sortable_list = [Visit.creation_time]
    name = "Посещения"
    name_plural = "Посещение"
    icon = "fa-regular fa-eye"
