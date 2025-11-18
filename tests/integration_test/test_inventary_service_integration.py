
def test_GetInventary_detail(client,db_session,Inventary_data):
    response = client.get('/Inventary/GetInventary_details')

    assert response.status_code == 200 
    assert response is not None
    data = response.json()
    assert data[0]["name"] == 'keyboard' 




