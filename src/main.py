from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from src.api import users, orders
from src.database.db import engine
from src.models.orm_models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User and Order API",
    description="API для управления пользователями и заказами",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "users",
            "description": "Операции с пользователями"
        },
        {
            "name": "orders",
            "description": "Операции с заказами"
        }
    ]
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="User and Order API",
        version="1.0.0",
        description="API для управления пользователями и заказами",
        routes=app.routes,
    )

    openapi_schema["info"]["contact"] = {
        "name": "Техническая поддержка",
        "url": "http://example.com/support",
        "email": "support@example.com",
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(users.router)
app.include_router(orders.router)


@app.get("/", tags=["status"])
def read_root():
    return {
        "service": "User and Order API",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
