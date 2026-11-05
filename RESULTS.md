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
- Step A4, status codes when the other user reads, changes and deletes:
## Part B
1.
2.
3.
4.
5.
6.
7.
8.