import serial
import pynmea2
from datetime import datetime

# --- ตั้งค่าการเชื่อมต่อ ---
SERIAL_PORT = 'COM4'   # เปลี่ยนเป็นหมายเลขพอร์ตของคุณ (เช่น 'COM3' หรือ '/dev/ttyUSB0')
BAUD_RATE = 38400       # อัตรา Baud rate (ลองเปลี่ยนเป็น 38400 หรือ 115200 หากข้อมูลไม่ออก)

# ตั้งชื่อไฟล์ Log ตามวันที่และเวลาที่เริ่มรันโปรแกรม
LOG_FILE = f"gps_raw_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def main():
    try:
        # เปิดการเชื่อมต่อ Serial Port
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"เชื่อมต่อกับ {SERIAL_PORT} สำเร็จ")
        print(f"กำลังเริ่มบันทึกข้อมูลทั้งหมดลงไฟล์: {LOG_FILE}")
        print("กด Ctrl+C เพื่อหยุดการทำงาน\n")

        # เปิดไฟล์ในโหมด Append ('a') เพื่อเขียนต่อท้ายไฟล์ไปเรื่อยๆ
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            while True:
                # อ่านข้อมูลทีละบรรทัดจากโมดูล GPS
                line_bytes = ser.readline()
                if not line_bytes:
                    continue
                
                # แปลงข้อมูลจาก Byte เป็น String
                try:
                    line = line_bytes.decode('ascii', errors='replace').strip()
                except Exception:
                    continue

                # ตรวจสอบว่าเป็นข้อมูล NMEA string ที่สมบูรณ์ (ขึ้นต้นด้วย $)
                if line.startswith('$'):
                    # สร้าง Timestamp ของคอมพิวเตอร์ ณ เวลาที่ได้รับข้อมูล (ละเอียดถึงระดับมิลลิวินาที)
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                    
                    # 1. บันทึกข้อมูลดิบลงไฟล์ Log
                    log_entry = f"[{timestamp}] {line}\n"
                    f.write(log_entry)
                    f.flush()  # บังคับให้เขียนลง Disk ทันที ป้องกันข้อมูลสูญหายหากโปรแกรมดับ

                    # 2. แสดงข้อมูลดิบทั้งหมดบนหน้าจอ Terminal
                    print(f"[RAW] {line}")

                    # 3. ส่วนเสริม: ลองถอดรหัส (Parse) ดูแบบคร่าวๆ บนหน้าจอ
                    try:
                        msg = pynmea2.parse(line)
                        # ดึงพิกัดจากประโยคที่มีค่า Latitude (เช่น GGA หรือ RMC)
                        if hasattr(msg, 'latitude') and msg.latitude != 0.0:
                            print(f"   -> [Parsed] พิกัด: {msg.latitude:.6f}, {msg.longitude:.6f}")
                        # ดึงค่าความเร็วจากประโยค RMC
                        if hasattr(msg, 'spd_over_grnd') and msg.spd_over_grnd is not None:
                            # แปลงหน่วยจาก Knots เป็น กิโลเมตร/ชั่วโมง (คูณ 1.852)
                            speed_kmh = msg.spd_over_grnd * 1.852
                            print(f"   -> [Parsed] ความเร็ว: {speed_kmh:.2f} km/h")
                    except pynmea2.ParseError:
                        pass  # ข้ามบรรทัดที่ข้อมูลมาไม่ครบถ้วน

    except serial.SerialException as e:
        print(f"\nเกิดข้อผิดพลาดในการเชื่อมต่อ Serial Port: {e}")
    except KeyboardInterrupt:
        print("\nหยุดการทำงานและปิดไฟล์ Log เรียบร้อยแล้วครับ")

if __name__ == '__main__':
    main()
