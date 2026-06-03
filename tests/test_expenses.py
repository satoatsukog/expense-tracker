def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_expense(client):
    payload = {
        "amount": "250.50",
        "category": "food",
        "description": "Lunch",
        "spent_on": "2025-06-01",
    }
    created = client.post("/expenses", json=payload)
    assert created.status_code == 201
    body = created.json()
    assert body["amount"] == "250.50"
    assert body["category"] == "food"

    fetched = client.get(f"/expenses/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["description"] == "Lunch"


def test_list_with_filters(client):
    client.post(
        "/expenses",
        json={"amount": "100", "category": "transport", "spent_on": "2025-06-10"},
    )
    client.post(
        "/expenses",
        json={"amount": "50", "category": "food", "spent_on": "2025-06-15"},
    )

    filtered = client.get(
        "/expenses",
        params={"category": "food", "date_from": "2025-06-01", "date_to": "2025-06-30"},
    )
    assert filtered.status_code == 200
    assert len(filtered.json()) == 1


def test_update_and_delete(client):
    created = client.post(
        "/expenses",
        json={"amount": "10", "category": "other"},
    ).json()

    updated = client.patch(f"/expenses/{created['id']}", json={"amount": "99.99"})
    assert updated.status_code == 200
    assert updated.json()["amount"] == "99.99"

    deleted = client.delete(f"/expenses/{created['id']}")
    assert deleted.status_code == 204
    assert client.get(f"/expenses/{created['id']}").status_code == 404


def test_monthly_report(client):
    client.post(
        "/expenses",
        json={"amount": "1000", "category": "housing", "spent_on": "2025-05-05"},
    )
    client.post(
        "/expenses",
        json={"amount": "200", "category": "food", "spent_on": "2025-05-20"},
    )

    report = client.get("/expenses/report/monthly", params={"year": 2025, "month": 5})
    assert report.status_code == 200
    data = report.json()
    assert data["total"] == "1200.00"
    assert len(data["by_category"]) == 2


def test_export_csv(client):
    client.post(
        "/expenses",
        json={"amount": "42", "category": "shopping", "description": "Book"},
    )
    response = client.get("/expenses/export.csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    text = response.text
    assert "id,date,category" in text
    assert "shopping" in text
    assert "Book" in text


def test_validation_rejects_negative_amount(client):
    response = client.post(
        "/expenses",
        json={"amount": "-1", "category": "food"},
    )
    assert response.status_code == 422
