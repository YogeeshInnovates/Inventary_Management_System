from fastapi import HTTPException
from app.models import Inventary_products,User_Pick_object,User,Products
from datetime import datetime ,timedelta 


def User_Picking_Datas(product_id ,data ,db ,user):
    user_id = user.id

    Inventary_product_datas = db.query(Inventary_products).filter(Inventary_products.product_id == product_id).first()

    # quantity_in_inventary = Inventary_product_datas.quantity_in_stock

    if Inventary_product_datas.quantity_in_stock <=0:
        raise HTTPException(status_code = 404, detail = "No product available")
    
    if Inventary_product_datas.quantity_in_stock < data.quantity_of_taking_product:
        raise HTTPException(status_code =409 ,detail = "No that much product available")
    
    if (Inventary_product_datas.quantity_taken_byuser +  data.quantity_of_taking_product) > Inventary_product_datas.quantity_in_stock :
        raise HTTPException(status_code = 409 ,detail = "User not able to get that much bacuse already taken by other user")
    
    Inventary_product_datas.quantity_taken_byuser += data.quantity_of_taking_product

    db.add(Inventary_product_datas)
    db.commit()
    db.refresh(Inventary_product_datas)


    pick = db.query(User_Pick_object).filter(User_Pick_object.user_id == user_id, User_Pick_object.product_id == product_id).first()

    if pick:
        pick.quantity_of_taking_product += data.quantity_of_taking_product
        pick.picking_date =datetime.now()
        pick.status_of_getting = "Not return"
        pick.return_date_time = None

    else:

        pick = User_Pick_object(

        Name_of_object_taker = data.Name_of_object_taker,
        product_id = product_id,
        quantity_of_taking_product = data.quantity_of_taking_product ,
        picking_date = datetime.now(),
        user_id =  user_id,
        status_of_getting = "Not return" ,
    )

    
        db.add(pick)

    db.commit()
    return {"message":"successfully taken by user"}


def User_return_Datas(product_id ,quantity_of_return_product ,status_usage  ,db ,user ):
    user_id = user.id

    if status_usage =="returned":
        User_return_data = db.query(User_Pick_object).filter(User_Pick_object.product_id == product_id,User_Pick_object.user_id == user_id).first()

        if User_return_data is None:
            raise HTTPException(status_code = 404,detail = "This user have not taken anything")
        if quantity_of_return_product > User_return_data.quantity_of_taking_product:
            raise HTTPException(status_code=400, detail="Return quantity exceeds picked quantity")


        User_return_data.quantity_of_taking_product -= quantity_of_return_product


        if User_return_data.quantity_of_taking_product==0:
            
            User_return_data.return_date_time= datetime.now()
        User_return_data.return_date_time =None

        if User_return_data.quantity_of_taking_product == 0:
            User_return_data.status_of_getting = "All return"
            

        Inventary_product_datas = db.query(Inventary_products).filter(Inventary_products.product_id == product_id).first()
    
        Inventary_product_datas.quantity_taken_byuser -= quantity_of_return_product
    

        db.commit()  # commit once
        db.refresh(User_return_data)
        db.refresh(Inventary_product_datas)
    elif status_usage =="used":
        User_return_data = db.query(User_Pick_object).filter(User_Pick_object.product_id == product_id,User_Pick_object.user_id == user_id).first()

        if User_return_data is None:
            raise HTTPException(status_code = 404,detail = "This user have not taken anything")
        if quantity_of_return_product > User_return_data.quantity_of_taking_product:
            raise HTTPException(status_code=400, detail="Return quantity exceeds picked quantity")



        User_return_data.quantity_of_taking_product -= quantity_of_return_product

        if User_return_data.quantity_of_taking_product==0:
            
            User_return_data.return_date_time= datetime.now()
        User_return_data.return_date_time =None

        if User_return_data.quantity_of_taking_product == 0:
            User_return_data.status_of_getting = "All return"


        Inventary_product_datas = db.query(Inventary_products).filter(Inventary_products.product_id == product_id).first()
    
        Inventary_product_datas.quantity_taken_byuser -= quantity_of_return_product

        Inventary_product_datas.quantity_in_stock -= quantity_of_return_product

        db.commit()  # commit once
        db.refresh(User_return_data)
        db.refresh(Inventary_product_datas)
    return {"message":"Successfully returned or updation done,Thank you "}



def getProductcarryUser_details(db):
    user_data = db.query(User).join(User.pick_object).all()
    datas = []

    for user in user_data:
        product_details = []

        for pick in user.pick_object:
            product = db.query(Products).filter(Products.id == pick.product_id).first()

            if product :
                product_details.append({

                    "product_name": product.name,
                        "quantity_taken": pick.quantity_of_taking_product,
                        "picking_date": pick.picking_date,
                        "status_of_getting": pick.status_of_getting,
                        "return_date": pick.return_date_time
                })
        datas.append({
            "user_id":user.id,
            "user_name":user.name,
            "product_taken":product_details
        })

    return datas


   

