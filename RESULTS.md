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
1. ความล้มเหลว 2 แบบที่การทดสอบกับเซิร์ฟเวอร์จริง (Real Server) ตรวจพบได้ แต่ Unit Test ที่ใช้ Stub ตรวจไม่พบ:
   - ปัญหาด้านเครือข่ายและ Load Balancer (เช่น Session ไม่คงที่/Sticky Session ขัดข้อง หรือการกระจายคำขอไปยังหลายเครื่องทำให้ข้อมูลซิงค์ไม่ทัน)
   - ปัญหาการเชื่อมต่อ (Integration/Schema) ระหว่างบริการจริงกับฐานข้อมูล เช่น Data Type ไม่ตรงกัน, ข้อจำกัดของ DB จริง, หรือข้อผิดพลาดตอน Serialize/Deserialize ข้อมูล
   เหตุผลที่ยังจำเป็นต้องเขียน Unit Test คู่ไปด้วย:
   - Unit Test ทำงานได้เร็วกว่ามาก ไม่ต้องพึ่งพาเครือข่ายหรือสถานะของเซิร์ฟเวอร์ภายนอก และสามารถระบุจุดที่โค้ดมีบั๊ก (Fault Localization) ได้อย่างเจาะจงโดยไม่มี Noise จากระบบเครือข่าย

2. ทำไมแต่ละเทสต้องสร้าง User ใหม่ของตัวเอง แทนการใช้ Public Token:
   - เพื่อให้เกิดความอิสระของชุดทดสอบ (Test Isolation) และป้องกันไม่ให้เกิด Race Condition หรือข้อมูลตีกัน เพราะหากใช้โทเค็นสาธารณะร่วมกัน ข้อมูลอาจถูกนักศึกษาคนอื่นหรือเทสตัวอื่นแก้ไข/ลบทิ้งระหว่างที่เทสกำลังรัน
   การนำแนวคิดนี้ไปประยุกต์ใช้ใน Project 2 (ระบบร้านค้าหรือโรงแรม):
   - ใน Project 2 ควรให้แต่ละกลุ่มหรือแต่ละเทสสร้าง Entity ของตัวเองแยกกันชัดเจน (เช่น ใช้ Prefix ชื่อผู้ใช้เฉพาะกลุ่ม หรือ Cart-Token ของตัวเอง) และจัดการเฉพาะข้อมูลที่เทสนั้นสร้างขึ้น พร้อมทำความสะอาด (Cleanup) ลบข้อมูลทิ้งหลังรันเสร็จ เพื่อไม่ให้กระทบข้อมูลกลุ่มอื่น

3. ทำไมเทสต้องส่งทุกคำขอผ่าน Session เดียวกัน:
   - QuickPizza มีเซิร์ฟเวอร์หลายเครื่องทำงานอยู่หลัง Load Balancer โดยแต่ละเครื่องเก็บข้อมูลผู้ใช้แยกกัน การใช้ `requests.Session` เดียวกันจะช่วยบันทึก Cookie (เช่น `AWSALB`, `AWSALBCORS`) ทำให้ Load Balancer ส่งคำขอต่อเนื่องทั้งหมดไปยังเซิร์ฟเวอร์เครื่องเดิมเสมอ
   ผลการทดลองใน Step 0.12 (ไม่ใช้ Session):
   - ผลการรัน 3 ครั้งล้มเหลวทั้งหมด (run 1: fail, run 2: fail, run 3: fail) โดยติด Error 401 Unauthorized ในขั้นตอนล็อกอิน เพราะคำขอล็อกอินถูกส่งไปยังเซิร์ฟเวอร์เครื่องอื่นที่ไม่รู้จัก User ที่เพิ่งสร้างขึ้น

4. การวิเคราะห์บั๊กใน Step 0.16 (Excluded Tools):
   - บล็อกที่เผยให้เห็น Defect: บล็อกที่ยกเว้นเครื่องมือครบทั้ง 3 ชนิด (`["Knife", "Pizza cutter", "Scissors"]`)
   - ทำไม 500 (Empty body) ถึงแย่กว่า 400 (มีข้อความ): Status 500 หมายถึงเซิร์ฟเวอร์เกิด Crash ภายในโดยไม่คาดคิด และการที่ Body ว่างเปล่าทำให้แอปพลิเคชันฝั่ง Client ไม่สามารถนำข้อความไปแสดงแจ้งผู้ใช้ได้ว่าส่งข้อมูลผิดพลาดอะไร ในขณะที่ 400 เป็นการบอกชัดเจนว่าคำขอผิดกฎ (เพราะไม่มีเครื่องมือตัดพิซซ่า)
   - ทำไมถึงคงเทสไว้ในชุดทดสอบเป็น xfail แทนที่จะลบทิ้ง: การใส่ `@pytest.mark.xfail(..., strict=True)` ช่วยบันทึกและติดตามข้อบกพร่องไว้ใน Test Suite โดยไม่ทำให้ CI/CD ล่ม และการมี `strict=True` จะคอยเตือนทันทีเมื่อทีมพัฒนาแก้ไขบั๊กนี้แล้ว (เทสจะกลายเป็น XPASS/Failed) เพื่อให้เราทราบและปรับปรุงเทสให้เป็นเทสปกติ

5. การคำนวณจำนวนเทสสำหรับโมเดลใน Step A1:
   - คุณลักษณะ (Characteristic) และจำนวนบล็อก:
     - C1 (ค่าดาว): 3 บล็อก
     - C2 (ชนิดของดาว): 4 บล็อก
     - C3 (พิซซ่ามีอยู่จริง): 2 บล็อก
     - C4 (โทเค็น): 3 บล็อก
   - Base Choice Coverage (BCC): 1 (Base Test ที่รวมบล็อกหลักทุกตัว) + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 1 + 2 + 3 + 1 + 2 = 9 เทส
   - All Combinations Coverage (AC): 3 * 4 * 2 * 3 = 72 เทส

6. รหัสสถานะ (Status Code) ใน Step A4 และการประเมิน:
   - รหัสสถานะที่ได้รับจริง:
     - อ่าน (Read): ได้ 404 Not Found (`{"error":"not found"}`)
     - แก้ไข (Update): ได้ 400 Bad Request (`{"error":"rating ID ... not found"}`)
     - ลบ (Delete): ได้ 400 Bad Request (`{"error":"rating ID ... not found"}`)
   - รหัสสถานะที่ควรจะเป็น: ควรได้ 404 (Not Found) หรือ 403 (Forbidden) สม่ำเสมอกันทุกกรณี
   - ถือว่าเป็น Defect หรือไม่: ถือว่าเป็น Defect ด้านความสอดคล้องตามมาตรฐาน HTTP (Inconsistent HTTP Semantics) เนื่องจากการหา Resource ไม่เจอหรือไม่มีสิทธิ์ไม่ควรตอบกลับเป็น 400 (ซึ่งหมายถึง Bad Request / Syntax ผิด) อย่างไรก็ตาม ในแง่ความปลอดภัยถือว่ายังปลอดภัยเพราะข้อมูลไม่ได้ถูกเปิดเผยหรือถูกแก้ไข

7. ผลการทดสอบด้วยโทเค็นสมมติ (`0000000000000000`):
   - สิ่งที่ได้รับกลับมา: เซิร์ฟเวอร์ตอบกลับด้วย `HTTP/2 200 OK` พร้อมรายการ Ratings ทั้งหมดของเซิร์ฟเวอร์นั้น
   - เป็น Defect หรือไม่: เป็น Defect ด้านความปลอดภัยที่ร้ายแรง (Authentication Bypass) เนื่องจากเซิร์ฟเวอร์ตรวจสอบเพียงแค่รูปแบบความยาวของโทเค็น (16 ตัวอักษร) แต่ไม่ได้ตรวจสอบว่าโทเค็นนั้นมีอยู่จริงในระบบหรือผูกกับ User ใด
   - ผลกระทบต่อระบบจริง: ผู้ไม่หวังดีสามารถสุ่มสร้างโทเค็น 16 ตัวอักษรขึ้นมาเองเพื่อข้ามการยืนยันตัวตน เข้าถึงข้อมูลที่เป็นส่วนตัว และอาจแก้ไขหรือลบข้อมูลในระบบจริงได้

8. การเปรียบเทียบ API Test กับ Web Page Test:
   - สิ่งที่ API Test ตรวจสอบได้ดีกว่า: ตรวจสอบความถูกต้องของ HTTP Status Code, Headers, โครงสร้างข้อมูล JSON Payload, Type ของข้อมูล และค่าขอบเขต (Boundary Values) ได้รวดเร็ว แม่นยำ และมีประสิทธิภาพกว่ามาก
   - สิ่งที่มีเฉพาะการทดสอบผ่านหน้าเว็บ (UI/Web Page Test) เท่านั้นที่ตรวจได้: การจัดวาง Layout และ CSS ที่แสดงผลบนหน้าจอจริง, ความ Responsive บนขนาดจอต่างๆ, การทับซ้อนของปุ่ม/องค์ประกอบ และประสบการณ์การใช้งานจริงของผู้ใช้ (User Experience / Accessibility)
