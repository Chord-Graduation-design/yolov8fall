  void onInit() {
    super.onInit();
    //订阅topic
    Iot().subscribe("esp32/aht10");
    Iot().subscribe("esp32/led");
    Iot().subscribe("esp32/servo");
    //注册AHT10回调用于接受温湿度信息
    Iot().addUpdateCallBack("esp32/aht10", (msg) {
      try {
        TemperatureAndHumidity x = TemperatureAndHumidity.fromBuffer(msg);
        temp.value = x.temperature;
        hum.value = x.humidity;
      } catch (e) {
        Get.log("esp32/aht10 ${e.toString()}");
      }
    });
    //注册led回调用于接受led开关信息
    Iot().addUpdateCallBack("esp32/led", (msg) {
      try{
        late var x = LedSwitch.fromBuffer(msg);
        led_switch.value = x.on;
      }catch(e){
        Get.log("esp32/led ${e.toString()}");
      }
    });
    //注册servo回调用于接受舵机角度信息
    Iot().addUpdateCallBack("esp32/servo", (msg) {
      try{
        late var x = ServoAngle.fromBuffer(msg);
        servo_angle.value = x.angle;
        Get.log("esp32/servo ${x.angle}");
      }catch(e)
      {
        Get.log("esp32/servo ${e.toString()}");
      }
    });
    // timer = Timer.periodic(const Duration(seconds: 1), temp_hum_get);
    //通知傻逼单片机,我tm来了 give me 信息
    SensorIn msg = SensorIn()..type = SensorType.IN_CONTROL;
    Iot().publish(Iot.InTopic,msg.writeToBuffer());
  }