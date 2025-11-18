# from fastapi import FastAPI
# from app.routers import auth,category_router,supplier_router,product_details_router,product_sales_router,user_control_forms_router,inventary_details_routers
# from apscheduler.schedulers.background import BackgroundScheduler
# from app.utils.email_sent import check_overdue_products
# import time
# from sqlalchemy.exc import OperationalError
# # Add these imports
# from app.database import Base, engine

# # Create all tables in database
# Base.metadata.create_all(bind=engine)
# # Wait until PostgreSQL is ready
# while True:
#     try:
#         with engine.connect() as conn:
#             print("Database is ready!")
#             break
#     except OperationalError:
#         print("Waiting for database...")
#         time.sleep(2)

# # Create tables
# Base.metadata.create_all(bind=engine)

# app=FastAPI()

# app.include_router(auth.router,prefix = "/auth",tags=["auth"])
# app.include_router(category_router.router,prefix="/category",tags=["Category"])
# app.include_router(supplier_router.router,prefix="/suppler_details",tags=["Supplier Entries and Details"])
# app.include_router(product_details_router.router,prefix="/product", tags=["Product Entries And Details"])
# app.include_router(product_sales_router.router,prefix="/sales",tags=["Sales Entries And Details"])
# app.include_router(user_control_forms_router.router,prefix = "/User_activity" , tags = ["User Activities and Info"])
# app.include_router(inventary_details_routers.router,prefix = "/Inventary",tags=["Inventary_Details"])

# schedular = BackgroundScheduler()
# schedular.add_job(check_overdue_products,'interval',minutes=3)
# schedular.start()





import time
from sqlalchemy.exc import OperationalError
from app.database import Base, engine
from fastapi import FastAPI
from app.routers import auth, category_router, supplier_router, product_details_router, product_sales_router, user_control_forms_router, inventary_details_routers
from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.email_sent import check_overdue_products

# # Wait until PostgreSQL is ready
# while True:
#     try:
#         with engine.connect() as conn:
#             print("Database is ready!")
#             break
#     except OperationalError:
#         print("Waiting for database...")
#         time.sleep(2)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(category_router.router, prefix="/category", tags=["Category"])
app.include_router(supplier_router.router, prefix="/suppler_details", tags=["Supplier Entries and Details"])
app.include_router(product_details_router.router, prefix="/product", tags=["Product Entries And Details"])
app.include_router(product_sales_router.router, prefix="/sales", tags=["Sales Entries And Details"])
app.include_router(user_control_forms_router.router, prefix="/User_activity", tags=["User Activities and Info"])
app.include_router(inventary_details_routers.router, prefix="/Inventary", tags=["Inventary_Details"])

schedular = BackgroundScheduler()
schedular.add_job(check_overdue_products, 'interval', minutes=3)
schedular.start()


