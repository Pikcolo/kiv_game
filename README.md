<img width="599" alt="2" src="https://github.com/Pikcolo/kiv_game/assets/153786025/56a42d6c-2dbd-4371-ba22-308f9b99973d"># Rocket Game

## Description about code (การทำงานของโค้ด)

### Thai 

    การทำงานโค้ดนี้เริ่มจาก Class GameWidget(Widget) ซึ่งเป็นส่วนที่ให้เกมทั้งหมดสามารถทำงานได้ และ
    การจัดองค์ประกอบต่าง ๆ ภายในเกมให้เหมาะสม โดยมี 

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

    นอกจากนี้ยังมีตัวแปรที่คอยกำหนดให้แสดงผลอย่างภาพพื้นหลัง 
    ข้อความคะแนน, เวลา,วิธีการเล่น การอัพเดทขนาดและตำแหน่ง

    ซึ่ง Class GameWidget จะมีความเชื่อมโยงกับ Class ที่เหลือต่อเพื่อให้เกมนี้สามารถเล่นได้
    โดย Class ที่มีส่วนเกียวข้องกับ Class Gamewidget ต่อ คือ


    - Class Entity(Object)
        
        - เป็น Class ที่กำหนดองค์ประกอบภายในเกมทั้งขนาด ตำแหน่ง ซึ่งเป็น Class สำคัญเป็นส่วนที่ทำให้ Player 
        สามารถใช้กระสุนยิงศัตรูหรือเหรียญเพื่อให้ได้คะแนน และการเกิดเอฟเฟคต่าง ๆ

    - Class Bullet(Entity)
       
        - เป็น Class ที่สืบทอดมาจาก Entity ใช้กำหนดการทำงานของกระสุนทั้งความเร็ว 
        ตำแหน่ง และรูป และมีฟังก์ชัน stop_callback ใช้หยุดการเรียกฟังก์ชันเคลื่อนที่
        อย่าง move_step ที่กำหนดการเคลื่อนที่ของกระสุนเพื่อให้จัดการการชนกับ 
        enemy หรือ coin อย่างถ้ายิง enemy ได้ 1 แต้ม แต่ถ้ายิง coin จะได้ 2 แต้ม

    - Class Enemy(Entity)
        
        - เป็น Class ที่สืบทอดมาจาก Enemy เช่นกัน ใช้กำหนดความเร็วในการเคลื่อนที่ ตำแหน่ง และความเร็ว ซึ่ง Class นี้
        และมีฟังก์ชัน stop_callback ใช้หยุดการเรียกฟังก์ชัน และใน move_step มีการกำหนดเงื่อนไขในการเคลื่อนที่เพิ่มด้วย 
        ซึ่งถ้าหากเคลื่อนที่ชนกับพื้นหรือขอบล่าง window จะเสียคะแนนไป 1 คะแนน

    - Class Explosion(Entity)
        
        - เป็น Class ที่สร้างองค์ประกอบการระเบิดขึ้นมา หลังเกิดการชนกันของ Object 
        และจะมีฟังก์ชันในการลบตัวเองออกหลังจากการเกิดการชน

    - Class Coin(Entity)
        
        - เป็น Class ที่มีความคล้าย Class Enemy แต่จะต่างกันตรงที่รูปภาพ ความเร็วเคลื่อนที่ และเมื่อ coin 
        ตกลงพื้นหรือขอบ window จะไม่เสียแต้มเหมือนกับ enemy

    - Class Player(Entity)
        
        - เป็น Class ที่กำหนดผู้เล่นทั้งรูปภาพ ตำแหน่ง ความเร็วของกระสุนที่ยิงออกมา มีฟังก์ชัน move_step 
        ใช้กำหนดปุ่มที่ใช้ในการควบคุมการเคลื่อนที่ของ player และ shoot_step ที่กำหนดปุ่มการยิงกระสุน

    - Class GameOverPopup(Popup):
        
        - เป็น Class ที่กำหนดการ popup ขึ้นมาหลังจากเวลาหมดโดยให้ popup 
        ขึ้นมาเพื่อให้ผู่เล่นสามารถกรอกข้อมูลหลังเล่นเกมจบก็จะมีให้กรอกชื่อ และการให้คะแนนตามข้อความที่ถาม 
        และเป็นคำถาม feedback เกี่ยวกับเกมและในส่วนคำถามที่ให้กรอกคะแนน ก็จะต้องกรอกเลขตามที่มีในคำถาม
        ไม่เช่นนั้น ก็จะมีข้อความเตือนออกมาว่าเป็นข้อมูลที่ผิดซึ่งจะต้องกรอกข้อมูลใหม่ซึ่งเป็นตัวเลข 
        โดยจะมีฟังก์ชัน dismiss_with_data และ show_error_message เป็นตัวจัดการข้อผิดพลาด

    
    และภายใน code จะมี

    game = GameWidget()
    game.player = Player()
    game.player.pos = (Window.width - Window.width/1.75, 0)
    game.add_entity(game.player)

    เป็นตัวกำหนดทำให้ตัวเกมสามารถเล่นได้ ซึ่งถ้าหาไม่มีตัวแปรนี้ก็จะทำให้เกมไม่สามารถเล่นได้ เนื่องจาใน code ส่วนนี้
    มีความเกี่ยวข้องกับในหลาย ๆ Class และจะต้องใช้ในการ return ค่า ใน Class RocketApp(App) ภายใน ฟังก์ชัน build

### Eng

    The code starts with the GameWidget() class, which is the part that makes the entire game work and 
    arranges the various elements within the game properly. It has the following functions

    - _update_size: A function that adjusts the size and position to fit the window.
    - spawn_enemies: Spawns enemies at random locations.
    - spawn_coins: Spawns coins at random locations.
    - on_frame: Sends the "on_frame" event, which is a function that can be overridden in subclasses.
    - update_time: Updates the remaining time in the game.
    - end_game: Schedules the end of the game, displays a pop-up with the final score, 
    and stops calling related functions.
    - store_score: A system for storing the final score after time runs out.
    - exit_app: A function for scheduling the exit of the application.
    - score: A function that is a property to get and set the game score.
    - add_entity: Adds an entity to the game.
    - remove_entity: Used to remove an entity from the game from the ongoing game process.
    - collides, colliding_entities: Used to check for collisions between entities.
    - on_keyboard_closed, on_key_down, on_key_up: Arranges the keyboard's operation 
    for both pressing and releasing keys.
    - The GameWidget class will be linked to the remaining classes to allow the game to be played.

    In addition to the classes described above, there are also variables 
    that are used to control the display of the game, such as the background image,
    the score text, the time, the instructions, and the update of the size and position.

    The GameWidget class is linked to the remaining classes to allow the game to be played. 
    The following classes are related to the GameWidget class:


    - Class Entity(Object)
        
        - This class defines the basic properties of all entities in the game, 
        such as size and position. It is important because it allows 
    the player to shoot bullets at enemies or coins to score points and trigger various effects.

    - Class Bullet(Entity)
        
        - The Bullet class inherits from the Entity class and defines the behavior of bullets,
        such as speed, position, and image. It also has a stop_callback function that can be used 
        to stop the call to the move_step function, which defines the movement of the bullet in 
        order to handle collisions with enemies or coins. For example,
        if a bullet collides with an enemy, it will score 1 point, 
        but if it collides with a coin, it will score 2 points.

    - Class Enemy(Entity)
        
        - The Enemy class inherits from the Entity class and defines the behavior of enemies, 
        such as speed,position, and image. It also has a stop_callback function that can be used to 
        stop the call to the move_step function.
        In the move_step function, there is an additional condition for movement, which is that 
        if the enemy moves and collides with the ground or the bottom edge of the window,
        it will lose 1 point.
    
    - Class Explosion(Entity)

        - The Explosion class creates an explosion element after an object collision. 
        It will also have a function to remove itself after the collision.
            
    
    - Class Coin(Entity)

        - The Coin class is similar to the Enemy class, but it differs in the image,
        movement speed, and the fact that when a coin falls to the ground or the edge of the window,
        it does not lose points like an enemy.

    - Class Player(Entity)

        - The Player class defines the player, including the image, position, and speed 
        of the bullets fired.It has a move_step function that defines the buttons used to
        control the player's movement and a shoot_step function that defines 
        the button for shooting bullets.

    - Class GameOverPopup(Popup)

        - The GameOverPopup class defines a popup that appears after the time runs out.
        The popup allows the player to enter information after the game is over,
        such as their name, a rating for the game, and feedback about the game.
        The rating question must be answered with a number. If the player enters a non-numeric value,
        an error message will be displayed. The dismiss_with_data and 
        show_error_message functions are used to handle errors.

    And in the code, there will be

    game = GameWidget()
    game.player = Player()
    game.player.pos = (Window.width - Window.width/1.75, 0)
    game.add_entity(game.player)

    These variables are essential for the game to function properly.
    They are used to initialize the game and to add the player to the game world.
    Without these variables, the game would not be able to play. Additionally,
    these variables are used in several classes and must be returned
    in the RocketApp(App) class within the build function.

## Running results (ผลการรัน)
<img width="598" alt="1" src="https://github.com/Pikcolo/kiv_game/assets/153786025/395e36db-6baf-4443-9efd-13371d6c9095">
<img width="597" alt="3" src="https://github.com/Pikcolo/kiv_game/assets/153786025/9d0b3c07-86a9-4393-927b-4fabc1c3a51b">
<img width="599" alt="2" src="https://github.com/Pikcolo/kiv_game/assets/153786025/27cf4021-18fb-404f-b7f8-b3e16da46a1f">
<img width="1280" alt="6" src="https://github.com/Pikcolo/kiv_game/assets/153786025/f0743372-7b69-4f74-835f-680034594ed7">
<img width="601" alt="4" src="https://github.com/Pikcolo/kiv_game/assets/153786025/0b048c0d-86e8-461f-9385-90ac3477c14c">
<img width="602" alt="5" src="https://github.com/Pikcolo/kiv_game/assets/153786025/172c7736-deb8-4ac5-bff0-c9abe8b707dc">
<img width="598" alt="7" src="https://github.com/Pikcolo/kiv_game/assets/153786025/9fef476d-5b90-47db-bf33-41f662969bc7">





