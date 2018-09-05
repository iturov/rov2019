# rov2019
İstanbul Teknik Üniversitesi ROV Takımı 2019

#### Branches:

* ~~raspberry-TCP~~
    - ~~TCP ile verileri ground station'a yollayacak modül~~
* ~~raspberry-serial~~
    - ~~serial ile STM32'ye verileri aktaracak modül~~
* ~~raspberry-main~~
    - ~~genel raspberry sistem yapısı~~
* [raspberry-extras](https://github.com/iturov/rov2019/tree/raspberry-extras "raspberry-extras")
    - raspberry üzerindeki geliştirmeler
    - ~~tüm exceptionları tek bir modülde toparlanacak~~
    - start.sh script'i yazılacak
* ~~[joystick](https://github.com/iturov/rov2019/tree/joystick "joystick")~~
    - ~~pygame.joystick ile değerler elde edilecek~~
    - TCP ile değerler rov'a yollanacak
* ~~[camera](https://github.com/iturov/rov2019/tree/camera "camera")~~
    - ~~raspberry'de gstreamer ile görüntü ground station'a yollanacak~~
* [GUI](https://github.com/iturov/rov2019/tree/GUI "GUI")
    - Kivy ile arayüz tasarlanacak
    - gstreamer'dan camera görüntüsü alınacak
    - ssh'dan raspberry terminali alınacak
    - joystick servisi arkaplanda çalışacak
* [stm-serial](https://github.com/iturov/rov2019/tree/stm-serial "stm-serial")
    - raspberry'den gelen data alınacak
    - raspberry'ye sensör datası yollanacak
* [stm-gpio](https://github.com/iturov/rov2019/tree/stm-gpio "stm-gpio")
    - esc, ışık, gripper PWM sinyali verilecek
    - sensör dataları okunacak
* [PID](https://github.com/iturov/rov2019/tree/PID "PID")
    - gelen joystick ve sensör datası kullanılarak gerekli PWM değerleri hesaplanacak
