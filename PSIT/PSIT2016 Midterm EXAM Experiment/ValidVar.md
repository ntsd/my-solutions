Exam6: ValidVar

เมื่อชื่อเสียงของคุณได้เลื่องลือออออ ระบืออออออนาม คุณก็เริ่มมีงานเข้ามา
และด้วยที่คุณนั้นเก่งกาจโปรแกรมมิ่งอย่างที่สุดจากโลกของคุณ ที่หาตัวจับยากในโลกคู่ขนาน(เพราะมีอยู่คนเดียว)
คุณจึงได้รับงานพิเศษเพิ่มขึ้นอีกงาน คือรับสอนเด็กในโรงเรียนเขียนโปรแกรม

เนื้อหาในวันนี้คือการตั้งชื่อตัวแปร
การตั้งชื่อตัวแปรนั้น มีกฎง่ายๆอยู่สี่ข้อ นอกเหนือจากกฎนี้แล้ว จะสามารถตั้งชื่อยาวเท่าไหร่ก็ได้ โดยที่ไม่ผิดไวยากรณ์
โดยที่ประกอบด้วยอักษรภาษาอังกฤษพิมพ์เล็ก และพิมพ์ใหญ่ และตัวเลข และ Underscore (_) โดยชื่อตัวแปรจะเป็น Case-Sensitive

1. ห้ามมีอักขระพิเศษผสมอยู่ในชื่อตัวแปร (Punctuation) เช่น % $ < เป็นต้น ยกเว้น Underscore _ ได้เท่านั้น
2. ห้ามมี white space  เช่น เว้นวรรค อยู่ภายในตัวแปร (ยกเว้น whitespace ด้านหน้าและด้านหลังของตัวแปร) 
3. ห้ามขึ้นตัวชื่อตัวแปรด้วยตัวเลข
4. ห้ามตั้งชื่อซ้ำกับคำสงวน (Reserved Word) โดยที่ Reserved Word มีหลายตัวดังนี้
if else elif while for True False continue break
return is in and or from as pass not def None

ซึ่งตามประสาเด็กๆ ก็จะตั้งชื่อตัวแปรมา แล้วให้คุณดูว่าชื่อดังกล่าวสามารถตั้งได้หรือไม่
แต่ว่าจำนวนเด็กที่ถามนั้นมีมากและบ่อยซะจนคุณขี้เกียจตรวจสอบด้วยตัวคุณเอง
คุณจึงเขียนโปรแกรมขึ้นมาเพื่อตรวจสอบว่า ชื่อตัวแปรที่เด็กส่งมานั้น สามารถใช้เป็นชื่อตัวแปรได้หรือไม่
 
by นายพิชาธร เอกอุ่น 
1 October 2016, 20:58
 Specification
 Input Specification	 Output Specification

1+n บรรทัด
บรรทัดแรก เป็นจำนวนชื่อตัวแปรที่ได้รับเข้ามา n
อีก n บรรทัดต่อมาเป็นชื่อตัวแปรที่ใช้ทดสอบ 

N บรรทัด
เป็นผลการทดสอบว่าชื่อตัวแปรนั้นสามารถใช้เป็นชื่อตัวแปรได้หรือไม่ตามลำดับที่ได้รับเข้ามา
Valid หากใช้ได้ หรือ Invalid หากไม่สามารถใช้ได้

  
 Sample Case
 Sample Input	 Sample Output
6
_velocity
parallel_planet
earth_v20b
Class
IfIWantToUseThisName
return
Valid
Valid
Valid
Valid
Valid
Invalid
20
tesseract
height
else
return
Elif
is_in_this_list
somalia
nonononononononononope
on_clock_12
Is
True
kilogram_in_%
mail@kmitl.ac.th
it59070001
true
lf
1valid
3_average_of_height
.hiddenfile
1122154484787974
Valid
Valid
Invalid
Invalid
Valid
Valid
Valid
Valid
Valid
Valid
Invalid
Invalid
Invalid
Valid
Valid
Valid
Invalid
Invalid
Invalid
Invalid
