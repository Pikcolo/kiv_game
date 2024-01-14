# Rocket Game

## Description about code (การทำงานในโค้ด)

- Thai 

    การทำงานโค้ดนี้เริ่มจาก Class GameWidget(Widget) ซึ่งเป็นส่วนที่ให้เกมทั้งหมดสามารถทำงานได้ และ
    การจัดองค์ประกอบต่าง ๆภายในเกมให้เหมาะสม โดยมี 

    - ฟังก์ชันที่ใช้ปรับขนาดและตำแหน่งให้เหมาะสมกับหน้าต่างอย่าง _update_size 
    - spawn_enemies : สร้างศัตรูขึ้นมาโดยการสุ่มเกิด
    - spawn_coins : สร้างเหรียญขึ้นมาโดยสุ่มตำแหน่ง
    - on-frame : ที่ส่งเหตุการณ์ "on_frame" ที่เป็นฟังก์ชันที่ทำให้ได้การแทนที่ใน SubClass
    - update_time : อัพเดทเวลาที่เหลืออยู่ในการเล่นเกม 
    - end_game : กำหนดการสิ้นสุดเกม แสดงป็อปอัปดับพร้อมคะแนนสุดท้าย และหยุดการเรียกฟังก์ชันที่เกี่ยวข้อง
    - store_score : ระบบเก็บคะแนนสุดท้ายหลังจากเวลาหมด
    - exit_app: ฟังก์ชันกำหนดการออกจากแอปพลิเคชัน
    - score: ฟังก์ชันที่เป็นคุณสมบัติเพื่อดึงข้อมูลและตั้งค่าคะแนนเกม
    - add_entity: เพิ่มองค์ประกอบเข้าสู่เกม
    - remove_entity: ใช้ลบองค์ประกอบออกจากเกมจากการดำเนินเการภายในเกม
    - collides, colliding_entities: ใช้ตรวจสอบการชนกันขององค์ประกอบ
    - on_keyboard_closed, on_key_down, on_key_up: จัดการทำงานของแป้นพิมพ์ทั้งการกดและปล่อยปุ่ม


    ซึ่ง Class GameWidget จะมีความเชื่อมโยงกับ Class ที่เหลือต่อเพื่อให้เกมนี้สามารถเล่นได้
    โดย Class ที่มีส่วนเกียวข้องกับ Class Gamewidget ต่อ คือ


    - Class Entity(Object)
        - เป็น Class ที่กำหนดองค์ประกอบภสยในเกมทั้งขนาด ตำแหน่ง ซึ่งเป็น Class สำคัญเป็นส่วนที่ทำให้ Player สามารถใช้กระสุนยิงศัตรูหรือเหรียญเพื่อให้ได้คะแนน และการเกิดเอฟเฟคต่าง ๆ

    - Class Bullet(Entity)
        - เป็น Class ที่สืบทอดมาจาก Entity ใช้กำหนดการทำงานของกระสุนทั้งความเร็ว ตำแหน่ง และรูป และมีฟังก์ชัน stop_callback ใช้หยุดการเรียกฟังก์ชันเคลื่อนที่อย่าง move_step ที่กำหนดการเคลื่อนที่ของกระสุนเพื่อให้จัดการการชนกับ enemy หรือ coin



- Eng

    The code starts with the GameWidget() class, which is the part that makes the entire game work and arranges the various elements within the game properly. 
    It has the following functions

    - _update_size: A function that adjusts the size and position to fit the window.
    - spawn_enemies: Spawns enemies at random locations.
    - spawn_coins: Spawns coins at random locations.
    - on_frame: Sends the "on_frame" event, which is a function that can be overridden in subclasses.
    - update_time: Updates the remaining time in the game.
    - end_game: Schedules the end of the game, displays a pop-up with the final score, and stops calling related functions.
    - store_score: A system for storing the final score after time runs out.
    - exit_app: A function for scheduling the exit of the application.
    - score: A function that is a property to get and set the game score.
    - add_entity: Adds an entity to the game.
    - remove_entity: Used to remove an entity from the game from the ongoing game process.
    - collides, colliding_entities: Used to check for collisions between entities.
    - on_keyboard_closed, on_key_down, on_key_up: Arranges the keyboard's operation for both pressing and releasing keys.
    - The GameWidget class will be linked to the remaining classes to allow the game to be played.


    The GameWidget class is linked to the remaining classes to allow the game to be played. The following classes are related to the GameWidget class:

    - Class Entity(Object)
        - This class defines the basic properties of all entities in the game, such as size and position. It is important because it allows the player to shoot bullets at enemies or coins to score points and trigger various effects.

    - Class Bullet(Entity)
        - This class inherits from the Entity class and defines the behavior of bullets, such as speed, position, and image. It also has a stop_callback function that can be used to stop the call to the move_step function, which defines the movement of the bullet in order to handle collisions with enemies or coins.