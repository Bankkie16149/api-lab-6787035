import pytest


# Boundary values of stars: 1 and 5 are saved, 0 and 6 are refused and the
# rating keeps its old stars (3 from the rating fixture).
@pytest.mark.parametrize(
    "stars, status",
    [(0, 400), (1, 200), (5, 200), (6, 400)],
)
def test_update_stars_boundaries(api, auth, rating, stars, status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == status
    saved = api.get(path, headers=auth).json()["stars"]
    expected = stars if status == 200 else rating["stars"]
    assert saved == expected
