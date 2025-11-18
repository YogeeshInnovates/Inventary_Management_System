
from app.models import Inventary_products

def GetInventary_detail(db):
    inventary_datas = db.query(Inventary_products).all()
    inventary_data_list_all = []
    for datas in inventary_datas:
        available_stock = datas.quantity_in_stock - datas.quantity_taken_byuser

        inventary_data_list={
            "id": datas.id,
        "product_id": datas.product_id,
        "sku": datas.sku,
        "quantity_in_stock": datas.quantity_in_stock,
        "name":datas.name,
        "quantity_taken_byuser": datas.quantity_taken_byuser,
        "Available_stok_in_Inventary":available_stock
        }

        inventary_data_list_all.append(inventary_data_list)
    return inventary_data_list_all



