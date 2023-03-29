# Application-for-automatic-music-genre-classification
แอปพลิเคชันนี้สามารถวิเคราะห์ประเภทของดนตรีอัตโนมัติโดยสามารถกําหนดประเภทของแนวดนตรีได้หลากหลายในหนึ่งดนตรีและสามารถใช้ผลลัพธ์จากการกําหนดประเภทของดนตรี เหล่านั้นไปใช้ตามประสงค์ของผู้ใช้อีกทั้งยังสามารถวิเคราะห์ความนิยมของดนตรีเบื้องต้นโดยการใช้ Application Program Interface ที่จะดึงแนวโน้มด้านต่างๆจากแอปพลิเคชันด้านดนตรีเพื่อมาวิเคราะห์เช่น ความนิยมของเพลงในสัปดาห์นั้นหรือวันนั้นๆเป็นต้น
# Installation
## ตัวโปรเจคใช้ภาษา python ##
เมื่อ download ไฟล์เสร็จทำการแตกไฟล์
 ****การที่จะให้ตัวโปรเจคสามารถใส่ไฟล์ MP4 เพื่อวิเคราะห์ไฟล์เพลงได้จำเป็นต้องมีไฟล์ ffmpeg**** \
 ****(ถ้าไม่ต้องการใช้ไฟล์ MP4 สามารถใช้งาน application ได้เลย)**** \
 ถ้าไม่มีต้อง download และ setpath ให้ถูกต้อง \
 สามารถ download ได้ที่ https://ffmpeg.org/download.html \
 ***tutorial ในการติดตั้ง หรือ setpath*** \
 For window Tutorial by Troblechute  https://www.youtube.com/watch?v=IECI72XEox0 \
 For Macos Totorial by Rickmakes https://www.youtube.com/watch?v=H1o6MWnmwpY \
สร้าง environment ในการใช้ติดตั้ง python pakage และรันคำสั่ง pip install -r requirements.txt ใน musicgenreapp folder
# วิธีใช้งาน
1.ทำการ run command prompt cd เข้าสู่ path ที่มี manage.py **|| cd FINAL-PROJECT-CPE-261492-main\musicgenreapp ||**  \
2.run command prompt **|| python manage.py runserver ||** \
3.เมื่อปรากฎลิ้งเข้าลิ้งเพื่อใช้งาน web application \
4.ทำการลงทะเบียนเพื่อใช้งาน **(สามารถใช้ demo username เพื่อเข้าไปลองใช้ได้ดังนี้ username:phumiwit, password Shoukugeki02)** \
5.web application สามารถใส่ไฟล์ได้สองประเภทคือ .wav และ mp4
# สำคัญ 
## เนื่องจากตัวโปรเจคได้มีการใช้งาน API จึงได้มีการซ่อนตัวของ API key ไว้ทำให้ไม่สามารถใช้งานฟังก์ชันดู 10 อันดับเพลงยอดนิยมได้ สามารถดูตัวอย่างการใช้งานฟังก์ชันต่างๆได้ที่ 
https://www.youtube.com/watch?v=MT1u_Gg4KII



