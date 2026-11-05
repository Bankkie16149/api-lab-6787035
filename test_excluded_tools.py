import pytest

# Blocks of "how many of the three tools are excluded":
# 0 tools, 1 tool, 2 tools (all work), and 3 tools (see the defect test below).


# The pizza never needs a tool that the customer excluded.
@pytest.mark.parametrize(
    "excluded",
    [[], ["Knife"], ["Scissors"], ["Knife", "Scissors"]],
)
def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# A request that no pizza can satisfy gets 400 and a JSON error, never 500.
@pytest.mark.xfail(
    reason="Defect 1: excluding all three tools makes /api/pizza answer "
           "500 with an empty body instead of 400 with a JSON error",
    strict=True,
)
def test_all_tools_excluded_is_refused(api, auth):
    body = {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()
