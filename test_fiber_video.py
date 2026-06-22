import cv2


def test_fiber_video():
    # 0 = กล้องตัวแรก (ส่วนใหญ่เป็นเว็บแคมโน้ตบุ๊ก)
    # ลองเปลี่ยนเป็น 1 หรือ 2 เพื่อเลือก USB Capture Card ที่ต่อมาจากไฟเบอร์
    camera_index = 1

    # เปิดการเชื่อมต่อกับกล้อง
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"[-] ไม่สามารถเปิดอุปกรณ์ที่ Index {camera_index} ได้ กรุณาตรวจสอบการเชื่อมต่อสาย USB")
        return

    print(f"[+] เชื่อมต่ออุปกรณ์ดัชนี {camera_index} สำเร็จ กำลังเปิดหน้าจอทดสอบ... (กด 'q' เพื่อปิด)")

    while True:
        # อ่านเฟรมภาพจาก Capture Card
        ret, frame = cap.read()

        # ถ้าดึงภาพสำเร็จ ret จะเป็น True
        if ret:
            # แสดงผลภาพบนหน้าต่าง Pop-up ของ OpenCV เองโดยตรง
            cv2.imshow("Fiber Optic Video Test Link", frame)
        else:
            print("[-] ไม่สามารถดึงเฟรมภาพได้ สัญญาณไฟเบอร์อาจจะขาดหาย หรือสายหลวม")
            break

        # รอการกดปุ่ม 'q' บนคีย์บอร์ดเพื่อออกจากลูปการทำงาน
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # คืนอุปกรณ์และปิดหน้าต่างทั้งหมดเมื่อเลิกใช้งาน
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    test_fiber_video()
