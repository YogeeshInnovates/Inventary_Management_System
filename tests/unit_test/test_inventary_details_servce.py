import pytest
from unittest.mock import MagicMock
from app.services.inventary_details_service import GetInventary_detail

@pytest.fixture
def mock_db():
    session = MagicMock()
    return session

class Inventarydata:
        id= 1
        product_id = 1
        sku = "HSR56"
        quantity_in_stock = 10
        name = "resberryphi"
        quantity_taken_byuser = 5
        Available_stok_in_Inventary = 0


def test_GetInventary_detail(mock_db):
    datas =  Inventarydata()

    mock_db.query.return_value.all.return_value = [datas]

    result = GetInventary_detail(mock_db)

    assert result[0]["Available_stok_in_Inventary"] == 5
