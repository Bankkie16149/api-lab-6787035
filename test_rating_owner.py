# A user must not read, change or delete the rating of another user.
# Each attempt must be refused (400 to 499) and leave the rating unchanged.


def owner_still_sees(api, auth, rating):
    res = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert res.status_code == 200
    assert res.json() == rating


# Another user cannot read the rating.
def test_other_user_cannot_read(api, auth, other_auth, rating):
    res = api.get(f"/api/ratings/{rating['id']}", headers=other_auth)
    assert 400 <= res.status_code <= 499
    owner_still_sees(api, auth, rating)


# Another user cannot change the stars of the rating.
def test_other_user_cannot_update(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": 1}, headers=other_auth)
    assert 400 <= res.status_code <= 499
    owner_still_sees(api, auth, rating)


# Another user cannot delete the rating.
def test_other_user_cannot_delete(api, auth, other_auth, rating):
    res = api.delete(f"/api/ratings/{rating['id']}", headers=other_auth)
    assert 400 <= res.status_code <= 499
    owner_still_sees(api, auth, rating)
