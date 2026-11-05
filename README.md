# api-lab: API testing with pytest and requests (ITDS362)

Tests for the QuickPizza API at https://quickpizza.grafana.com.

## Install and run
```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -v
pytest -v --html=report.html --self-contained-html   # HTML report
```
Every test creates its own user, so the tests do not depend on each other.

## Input domain model for POST /api/ratings

| Characteristic | Block | Value in the test | Test that covers it |
|---|---|---|---|
| C1 Value of stars | below 1 | 0 | `test_stars_out_of_range[0]` |
| | 1 to 5 (base) | 3 | `test_base_choice_is_saved` |
| | above 5 | 6 | `test_stars_out_of_range[6]` |
| C2 Type of stars | whole number (base) | 3 | `test_base_choice_is_saved` |
| | decimal | 3.5 | `test_stars_decimal_is_refused` |
| | text | "3" | `test_stars_text_is_refused` |
| | missing | no field | `test_stars_missing_is_refused` |
| C3 Pizza | exists (base) | a new pizza | `test_base_choice_is_saved` |
| | does not exist | 999999999 | `test_unknown_pizza_is_refused` |
| C4 Token | the user's own (base) | from auth | `test_base_choice_is_saved` |
| | none | no header | `test_no_token_is_refused` |
| | wrong length | token abc | `test_short_token_is_refused` |

Base choice coverage needs 1 + 2 + 3 + 1 + 2 = 9 tests (the 9 tests in
`test_create_rating.py`). All combinations would need 3 x 4 x 2 x 3 = 72.

## Other files
- `test_update_rating.py`: boundary values 0, 1, 5, 6 for PUT /api/ratings/{id}
- `test_rating_owner.py`: another user may not read, change or delete a rating
- `test_excluded_tools.py`: includes the xfail test for Defect 1 (see RESULTS.md)
