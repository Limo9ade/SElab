import pytest
from fastapi.testclient import TestClient
from main import api, tickets, Ticket  

client = TestClient(api)


@pytest.fixture(autouse=True)
def clear_tickets():
    tickets.clear()
    yield
    tickets.clear()


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Ticket Booking System"}


def test_add_ticket():
    ticket_data = {
        "id": 1,
        "flight_name": "Flight A",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Dhaka"
    }
    response = client.post("/ticket", json=ticket_data)
    assert response.status_code == 200
    assert response.json() == ticket_data
    assert len(tickets) == 1


def test_get_tickets():
    ticket = Ticket(id=1, flight_name="Flight A", flight_date="2025-10-15",
                    flight_time="14:30", destination="Dhaka")
    tickets.append(ticket)
    
    response = client.get("/ticket")
    assert response.status_code == 200
    assert response.json() == [ticket.dict()]


def test_update_ticket_success():
    ticket = Ticket(id=1, flight_name="Flight A", flight_date="2025-10-15",
                    flight_time="14:30", destination="Dhaka")
    tickets.append(ticket)
    
    updated_data = {
        "id": 1,
        "flight_name": "Flight B",
        "flight_date": "2025-10-20",
        "flight_time": "16:00",
        "destination": "Chittagong"
    }
    response = client.put("/ticket/1", json=updated_data)
    assert response.status_code == 200
    assert response.json() == updated_data
    assert tickets[0].flight_name == "Flight B"


def test_update_ticket_not_found():
    updated_data = {
        "id": 1,
        "flight_name": "Flight B",
        "flight_date": "2025-10-20",
        "flight_time": "16:00",
        "destination": "Chittagong"
    }
    response = client.put("/ticket/1", json=updated_data)
    assert response.status_code == 200
    assert response.json() == {"error": "Ticket Not Found"}


def test_delete_ticket_success():
    ticket = Ticket(id=1, flight_name="Flight A", flight_date="2025-10-15",
                    flight_time="14:30", destination="Dhaka")
    tickets.append(ticket)
    
    response = client.delete("/ticket/1")
    assert response.status_code == 200
    assert response.json() == ticket.dict()
    assert len(tickets) == 0


def test_delete_ticket_not_found():
    response = client.delete("/ticket/1")
    assert response.status_code == 200
    assert response.json() == {"error": "Ticket not found, deletion failed"}
