import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

from admin_panel.admin_models import (CustomerAdmin, OrderAdmin, StoreAdmin,
                                      VisitAdmin, WorkerAdmin)
from apps.order.routers import order_router
from apps.visit.routers import visit_router
from apps.worker.routers import worker_router
from apps.customer.routers import customer_router
from db.session import engine

app = FastAPI(title='test_app')

app.include_router(worker_router)
app.include_router(order_router)
app.include_router(visit_router)
app.include_router(customer_router)

admin = Admin(app, engine)

admin.add_view(WorkerAdmin)
admin.add_view(CustomerAdmin)
admin.add_view(StoreAdmin)
admin.add_view(OrderAdmin)
admin.add_view(VisitAdmin)

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
