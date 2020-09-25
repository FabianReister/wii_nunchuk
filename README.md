# ROS driver for Wii Nunchuk (remote controller)

This package reads out the Wii Nunchuk remote controller sensors including the accelerometer and the buttons.

![https://upload.wikimedia.org/wikipedia/commons/b/b6/Wii_Remote_%26_Nunchuk.jpg](https://upload.wikimedia.org/wikipedia/commons/b/b6/Wii_Remote_%26_Nunchuk.jpg)


## Prerequisites

- Wii Nunchuk remote controller (shown on the right in the image above)
- Arduino Board (e.g. Uno, Nano, ...)

## Hardware setup

- First, connect the Nunchuk remote controller to the Arduino board. This might require the removal of the connector. For further details, see [1]. 

General wiring scheme:
- connect power supply: 3.3V and GND
- connect I2C clock and data signals

- Then, connect the Arduino board and the computer

## Software setup

### Arduino

Within the "wii_nunchuk/assets" folder you will find and Arduino sketch file. Follow the instructions in the README located in that directory and upload the sketch. 

### ROS

Make sure, this folder is part of a catkin workspace. If so, run

    catkin build wii_nunchuk
  
## Usage

After setup, you can launch the ROS node

    roslaunch wii_nunchuk nunchuk.launch
  
It might be required, that you change some parameters depending on your OS. The parameters are within the launch file.


Once, the node is properly running, the sensor readings will be published on the "nunchuk" topic as a NunchukMsg, which is

    geometry_msgs/Vector3 acceleration_raw # raw accelerometer readings
    geometry_msgs/Vector3 acceleration_calibrated  # calibrated acceleration
    bool button_c # True if button is pressed
    bool button_z
    float32[2] joy_calibrated # the joy stick x and y signal

    float32[2] angles # euler angles



## Links

- [1] https://www.makerblog.at/2016/01/wii-nunchuk-controller-am-arduino-teil-1/ (How to connect Nunchuk controller to Arduino board, German)
