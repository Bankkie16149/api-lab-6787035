# api-lab: API testing with pytest and requests (ITDS362)

ชุดการทดสอบ API ของ QuickPizza (https://quickpizza.grafana.com) สำหรับวิชา ITDS362 Software Quality Assurance and Testing

สำหรับรายละเอียดผลการทดสอบทั้งหมด, รายงานข้อบกพร่อง (Defect Report), และคำตอบส่วนข้อคำถาม (Part B) สามารถดูได้ที่ [RESULTS.md](RESULTS.md) รวมทั้งดูรายงานสรุปผลการรันเทสฉบับสมบูรณ์ได้จากไฟล์ [report.html](report.html)

---

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

Base choice coverage needs 1 + 2 + 3 + 1 + 2 = 9 tests (the 9 tests in `test_create_rating.py`). All combinations would need 3 x 4 x 2 x 3 = 72.

## Overview of Test Files
- `test_create_rating.py`: ครอบคลุม Base Choice Coverage จาก Input Space Partitioning สำหรับการสร้าง Rating
- `test_update_rating.py`: ทดสอบ Boundary Values (0, 1, 5, 6) สำหรับ PUT /api/ratings/{id}
- `test_rating_owner.py`: ทดสอบสิทธิ์การเข้าถึงข้อมูลของ Rating (ไม่อนุญาตให้ผู้ใช้อื่นอ่าน แก้ไข หรือลบ)
- `test_excluded_tools.py`: ทดสอบการยกเว้นเครื่องมือ และตรวจจับ Defect กรณีที่ยกเว้นครบทุกเครื่องมือ (xfail)
- `test_refused.py`: ทดสอบกรณี Request ที่ต้องถูกปฏิเสธ (Username ซ้ำ, รหัสผิด, ชื่อว่าง)
- `test_names.py`, `test_tools.py`, `test_pizza.py`, `test_users.py`: ชุดทดสอบพื้นฐานและตรวจสอบ Token / User ratings
