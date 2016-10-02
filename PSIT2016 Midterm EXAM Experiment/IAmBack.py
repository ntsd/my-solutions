"""Exam10: IAmBack

คุณได้กลับถึงโลกแล้ว ไม่รู้เหมือนกันว่าข้ามข้อไหนมาบ้าง

โลกตอนนี้เปลี่ยนไป มีแต่คนเขียนได้แค่ภาษาไทย กับภาษาอังกฤษ

และคุณต้องทักทายคนในโลกของคุณเป็นภาษาตามที่เขาเขียนทักมา เช่น

ถ้าเค้าบอกว่าเค้าชื่อ สมหมาย คุณต้องตอบเค้าไปว่า สวัสดี สมหมาย

แต่เค้าทักมาว่าเค้าชื่อ world คุณต้องตอบเค้าไปว่า Hello world. 
(สังเกตว่าคุณเป็นคนที่แม่น Grammar ว่าถ้าตอบภาษาอังกฤษต้องมี full stop ต่อท้ายประโยคด้วย)

 
by นายพิชาธร เอกอุ่น 
1 October 2016, 20:58
 Specification
 Input Specification	 Output Specification

1 บรรทัด เป็นคำที่ เป็นภาษาไทย หรือ ภาษาอังกฤษ อย่างใดอย่างนึง ไม่มีผสม 

1 บรรทัดเป็นข้อความที่ตอบกลับไป 
 Sample Case
 Sample Input	 Sample Output
World
Hello World.
สมหมาย
สวัสดี สมหมาย"""
def iamback(word):
    """..."""
    letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("Hello "+word+"." if word[0] in letter+letter.lower() else "สวัสดี "+word)
iamback(input())
