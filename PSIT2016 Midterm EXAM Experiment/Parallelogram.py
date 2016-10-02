"""Exam7: Parallelogram

คุณอยู่ที่โลกคู่ขนานนานเสียจนคุณอยากจะไปตัดผมทรงใหม่ ให้เป็นทรงที่ฮิตกันในชนบทโลกคู่ขนาน
ในขณะที่ช่างตัดผมกำลังตัดผมให้คุณนั้น เขาได้บ่นถึงป้ายร้านอันเก่าของเขาที่ดูล้าสมัย ที่เป็นเพียงป้ายข้อความดาษๆเท่านั้น เขาอยากได้ป้ายใหม่ที่ดูเก๋ไก๋ มีไฟหมุนๆ
ด้วยที่คุณก็อยากได้เงินเพิ่ม จึงลองรับงานนี้ดู คิดเสียว่าเป็นค่าตัดผม

เจ้าของร้านบอกว่า
- ยังไงก็ได้ ง่ายๆ แต่ขอดูเก๋ๆ
- มีดีไซน์
- แสดงเป็นชื่อร้าน
- อยากได้ชื่อร้าน อยู่บนป้ายซ้ำๆหลายๆครั้ง ให้ลูกค้าติดตา
- ไม่แสดงชื่อร้านแนวนอน มันดูเรียบง่าย
- ไม่เอาแนวตั้งแบบสี่เหลี่ยมด้วย เพราะว่ามันให้ความรู้สึกแข็งกระด้าง
- เอาเอียงๆ สีไม่ต้อง
- เอียงๆทำมุม 45 องศา
- สอดแทรกคำคม Stay hungry Stay foolish.....
 
- ..........................................................งง

คุณจึงลองส่งข้อความตัวอย่างให้เจ้าของร้านดู แล้วให้เจ้าของร้านเขียนออกมาให้ดู ว่าต้องการแบบไหน
แล้วให้คุณเขียนโปรแกรมแสดงผลให้แสดงผลเหมือนกับที่เจ้าของร้านต้องการ
ดูได้จาก Sample I/O
 
by นายพิชาธร เอกอุ่น 
1 October 2016, 20:58
 Specification
 Input Specification	 Output Specification

หนึ่งบรรทัด เป็นข้อความทดสอบ

  

ขนาดของข้อความ * 2  - 1 บรรทัด เป็นข้อความป้ายร้านตามแบบที่เจ้าของร้านกำหนด

  
 Sample Case
 Sample Input	 Sample Output
SampleText
         S
        Sa
       Sam
      Samp
     Sampl
    Sample
   SampleT
  SampleTe
 SampleTex
SampleText
ampleText
mpleText
pleText
leText
eText
Text
ext
xt
t
Sample I/O
         S
        Sa
       Sam
      Samp
     Sampl
    Sample
   Sample
  Sample I
 Sample I/
Sample I/O
ample I/O
mple I/O
ple I/O
le I/O
e I/O
 I/O
I/O
/O
O"""
def parallelogram(text):
    """..."""
    lenght = len(text)
    for i in range(1, lenght):
        print(" "*(lenght-i)+text[:i])
    for i in range(lenght):
        print(text[i:])
parallelogram(input())
