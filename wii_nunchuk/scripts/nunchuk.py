#!/usr/bin/env python

import rospy
from geometry_msgs.msg import TransformStamped
from serial import Serial, SerialException

from wii_nunchuk.msg import nunchuk as NunchukMsg
import tf2_ros

import tf_conversions

def parse_msg(raw_msg: str) -> NunchukMsg:
    els = raw_msg.split(',')

    assert len(els) == 10

    """
     nunchuk_accelx(), 
    nunchuk_accely(), 
    nunchuk_accelz(), 
    nunchuk_caccelx(), 
    nunchuk_caccely(), 
    nunchuk_caccelz(),
    nunchuk_cjoy_x(),
    nunchuk_cjoy_y(), 
    nunchuk_zbutton(), 
    nunchuk_cbutton());
    
    
    
    """

    acc_x = int(els[0])
    acc_y = int(els[1])
    acc_z = int(els[2])

    cacc_x = int(els[3])
    cacc_y = int(els[4])
    cacc_z = int(els[5])

    import numpy as np
    roll = np.math.atan2(cacc_x, cacc_z)
    pitch = np.math.atan2(cacc_y, cacc_z)


    msg = NunchukMsg()
    msg.acceleration_raw.x = float(acc_x)
    msg.acceleration_raw.y = float(acc_y)
    msg.acceleration_raw.z = float(acc_z)
    msg.acceleration_calibrated.x = float(cacc_x)
    msg.acceleration_calibrated.y = float(cacc_y)
    msg.acceleration_calibrated.z = float(cacc_z)
    msg.joy_calibrated[0] = float(els[6])
    msg.joy_calibrated[1] = float(els[7])
    msg.button_c = bool(int(els[8]))
    msg.button_z = bool(int(els[9]))

    msg.angles = [roll, pitch]

    return msg


def main():
    rospy.init_node('nunchuk', anonymous=True)

    port = rospy.get_param("~port")
    baudrate = rospy.get_param("~baudrate")

    ser = None
    try:
        ser = Serial(port, baudrate, timeout=1)
    except SerialException:
        if not ser:
            rospy.logwarn("Serial port %s not available!" % port)
            return

        "The port is at use"
        ser.close()
        ser.open()

    # discard the first message, might not be complete
    ser.readline()

    pub = rospy.Publisher('nunchuck', NunchukMsg, queue_size=10)
    # rate = rospy.Rate(10)  # 10hz

    br = tf2_ros.TransformBroadcaster()


    try:
        while not rospy.is_shutdown():
            msg_in = ser.readline()
            msg_out = parse_msg(msg_in.decode("utf-8"))
            time = rospy.get_time()
            # rospy.loginfo(hello_str)
            pub.publish(msg_out)


            t = TransformStamped()
            t.header.stamp = rospy.Time.now()
            t.header.frame_id = "nunchuk_base"
            t.child_frame_id = "nunchuck"

            q = tf_conversions.transformations.quaternion_from_euler(msg_out.angles[0], msg_out.angles[1], 0.0 )
            t.transform.rotation.x = q[0]
            t.transform.rotation.y = q[1]
            t.transform.rotation.z = q[2]
            t.transform.rotation.w = q[3]

            br.sendTransform(t)

            # rate.sleep()
    #except Exception as ex:
    except rospy.ROSInterruptException as ex:
        print("exception...")
        print(str(ex))
        if ser is not None:
            ser.close()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException as ex:
        print(str(ex))
