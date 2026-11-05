import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


# Base choice: 3 stars as a whole number, a real pizza, the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id


# C1: a number of stars below 1 or above 5 is refused with a message.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C2: stars as a decimal number is refused, the API wants a whole number.
def test_stars_decimal_is_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3.5}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert "cannot unmarshal number 3.5" in res.json()["error"]


# C2: stars as text is refused, even when the text looks like a number.
def test_stars_text_is_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": "3"}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert "cannot unmarshal string" in res.json()["error"]


# C2: a rating without the stars field is refused like a rating with 0 stars.
def test_stars_missing_is_refused(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C3: a pizza that does not exist is refused with a message.
def test_unknown_pizza_is_refused(api, auth):
    new = {"pizza_id": 999999999, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": "pizza ID 999999999 not found"}


# C4: a request without the Authorization header is refused with 401.
def test_no_token_is_refused(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new)
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}


# C4: a token of the wrong length is refused with 401.
def test_short_token_is_refused(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    short = {"Authorization": "token abc"}
    res = api.post("/api/ratings", json=new, headers=short)
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}
