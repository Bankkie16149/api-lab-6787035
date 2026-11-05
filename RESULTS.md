# API lab results
## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza:  A Little Prosciutto
- Step 0.12, results of the three runs without a session (optional): run1 : fail run2 : fail run3 : fail
- Step 0.16, blocks of "how many of the three tools are excluded": 0 tools (200), 1 tool (200), 2 tools (200), 3 tools (500, defect). The original test covered only the 1-tool block, so I added [] and ["Knife", "Scissors"], and moved the 3-tool input to its own xfail test.
## Defect report
- Title: Defect 1: excluding all three tools makes POST /api/pizza answer 500 with an empty body
- Request: POST https://quickpizza.grafana.com/api/pizza with header `Authorization: token abcdef0123456789` and body `{"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}` (all_tools.json)
- Expected result: status 400 and a JSON error message, because no pizza can be cut without a tool
- Actual result: status 500 (Internal Server Error) with content-length 0 and an empty body
- Severity: Medium. The server fails on input the client controls, and the empty body gives the calling app no message to show. It affects one rare input and no data is lost.

## Part A
- Step A4, status codes when the other user reads, changes and deletes: read 404 (`not found`), change 400 (`rating ID ... not found`), delete 400 (`rating ID ... not found`). In every case the owner still reads the same rating afterwards.
## Part B
1. Two kinds of failures that tests against a real server can find (which unit tests with stubs cannot):
   - Network / load balancer issues (such as session stickiness failures and routing across multiple server instances).
   - Integration / schema mismatches with the real backend service, database constraints, or live serialization bugs.
   Reason to still write unit tests with stubs:
   - Unit tests are extremely fast to execute, do not depend on external network stability or live server availability, and isolate the exact location of a code fault directly without network noise.

2. Why each test creates its own user:
   - To ensure test isolation and prevent race conditions or data collisions. If tests shared a public token or account, concurrent runs or other students could alter, overwrite, or delete ratings while a test is executing.
   Application to Project 2 (shared shop or hotel):
   - For Project 2, each test suite or test case should register its own unique user/entity (e.g. unique username prefix or cart token) and only manipulate or assert data created by itself, cleaning up after execution to avoid interfering with other groups.

3. Why tests send every request through one session:
   - QuickPizza operates multiple server instances behind a load balancer, and user state/memory is not shared instantly across all instances. Using a single `requests.Session` retains cookies (such as `AWSALB` and `AWSALBCORS`), which forces the load balancer to route all sequential requests from that session to the same backend server.
   Step 0.12 run results:
   - In Step 0.12 without a session, all three test runs failed (run1: fail, run2: fail, run3: fail) with 401 Unauthorized because the subsequent login request was routed to a server instance that had not processed the user creation request.

4. Excluded tools block and defect explanation:
   - Block that revealed the defect: The block where all 3 tools are excluded (`["Knife", "Pizza cutter", "Scissors"]`).
   - Why 500 with empty body is worse than 400 with a message: A 500 error signifies an unhandled server crash/exception, leaving client applications without any actionable error message to inform the user what went wrong. A 400 with a descriptive JSON message clarifies that the client sent an impossible request (no pizza can be cut without a tool).
   - Why keep the test as xfail: Keeping it marked with `@pytest.mark.xfail(..., strict=True)` documents the defect within the test suite without breaking the build/CI pipeline. With `strict=True`, if the backend developers ever fix the bug, pytest will fail (XPASS), immediately notifying the QA engineer to update the test expectation and remove the mark.

5. Test count calculation for Step A1 model:
   - Characteristics and blocks:
     - C1 (Value of stars): 3 blocks
     - C2 (Type of stars): 4 blocks
     - C3 (Pizza exists): 2 blocks
     - C4 (Token): 3 blocks
   - Base Choice Coverage (BCC): 1 (base test covering all base blocks) + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 1 + 2 + 3 + 1 + 2 = 9 tests.
   - All Combinations Coverage (AC): 3 * 4 * 2 * 3 = 72 tests.

6. Status codes in Step A4 and evaluation:
   - Observed status codes:
     - Read: 404 Not Found (`{"error":"not found"}`)
     - Update: 400 Bad Request (`{"error":"rating ID ... not found"}`)
     - Delete: 400 Bad Request (`{"error":"rating ID ... not found"}`)
   - Expected status codes: Ideally 404 (Not Found) or 403 (Forbidden) for unauthorized resource access on another user's rating.
   - Is it a defect? Yes, returning 400 (Bad Request) for missing/inaccessible resource operations is an inconsistency and misuse of HTTP semantics (400 represents malformed syntax/bad request parameters, whereas non-existent or inaccessible IDs should return 404 or 403). However, security-wise the resource remains protected as the rating was neither disclosed nor modified.

7. Test with made-up token (`0000000000000000`):
   - What comes back: Status `HTTP/2 200 OK` returning the full list of all ratings stored on that server instance (`{"ratings":[...]}`).
   - Is this a defect? Yes, it is a significant authentication/authorization bypass defect. The API server only validates that the token string exists and satisfies a 16-character length constraint, without verifying whether the token actually corresponds to an authenticated session or valid user in the database.
   - Potential impact on a real system: An unauthorized attacker or stranger could craft arbitrary dummy tokens to bypass authentication, inspect sensitive ratings or customer records, and potentially compromise system privacy.

8. Comparison between API tests and UI/Web page tests:
   - What API tests check better: API tests verify HTTP status codes, response headers, precise payload schemas/data types, raw error structures, and boundary values much faster and more reliably without UI overhead.
   - What only web page tests can check: Visual layout and rendering (e.g. CSS, responsive design, overlapping elements), client-side interactivity, accessibility (a11y), and true end-to-end user experience within an actual web browser.
