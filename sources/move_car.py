#! /usr/bin/env python3

import rospy
import math
import tf
import sys
import select
import tty
import termios
from gazebo_msgs.msg import ModelState, ModelStates
from geometry_msgs.msg import Pose
from tf.transformations import euler_from_quaternion, quaternion_from_euler

model_name = 'hatchback_red'

class CarController:
    def __init__(self):
        # 初始化节点
        rospy.init_node('car_keyboard_controller')

        # 控制参数
        self.target_yaw = 0.0    # 目标偏航角（弧度）
        self.current_yaw = 0.0   # 当前实际偏航角

        self.current_roll = 0.0 
        self.current_pitch = 0.0 

        self.speed = 0.0  # 当前线速度（m/s）
        self.angular_speed = 0.2 # 角速度（rad/s）
        
        # 控制参数配置
        self.max_speed = 2.0     # 最大速度
        self.acc_step = 0.2      # 加速度步长
        self.yaw_step = math.radians(10)  # 偏航角调整步长（30度）

        # 模型位置
        self.pose = Pose()

        # 初始化订阅者（获取模型姿态）
        self.model_states_sub = rospy.Subscriber('/gazebo/model_states', ModelStates, self.model_states_callback)

        # 初始化发布者（速度控制）
        self.pos_pub = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=10)

        # 等待获取初始姿态
        rospy.loginfo("Waiting for initial pose...")
        rospy.wait_for_message("/gazebo/model_states", ModelStates)
        rospy.loginfo("Controller ready!")

    def model_states_callback(self, msg: ModelStates):
        # 更新模型状态
        model_index = msg.name.index(model_name)
        self.pose = msg.pose[model_index]

        # 四元数转欧拉角
        (roll, pitch, yaw) = euler_from_quaternion([
            self.pose.orientation.x,
            self.pose.orientation.y, 
            self.pose.orientation.z,
            self.pose.orientation.w
        ])
            
        # 更新当前偏航角（保持-π到π范围）
        self.current_yaw = math.atan2(math.sin(yaw), math.cos(yaw))
        self.current_roll = math.atan2(math.sin(roll), math.cos(roll))
        self.current_pitch = math.atan2(math.sin(pitch), math.cos(pitch))
            
        # 初始化目标偏航角
        if self.target_yaw == 0.0:
            self.target_yaw = self.current_yaw


    def get_key(self):
        # 非阻塞获取键盘输入
        tty.setraw(sys.stdin.fileno())
        rlist = select.select([sys.stdin], [], [], 0.1)[0]
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def on_key_press(self, key):
        # 键盘事件处理
        if key == 'w' or key == 'W':    # 加速
            self.speed = min(self.speed + 0.5, 10.0)
        elif key == 's' or key == 'S':  # 减速
            self.speed = max(self.speed - 0.5, -10.0)
        elif key == 'a' or key == 'A':  # 左转
            self.target_yaw += self.angular_speed * 0.1
        elif key == 'd' or key == 'D':  # 右转
            self.target_yaw -= self.angular_speed * 0.1
        elif key == '0':
            self.speed = 0
        

    def control_loop(self):
        # 控制循环
        rate = rospy.Rate(100)
        dt = 0.01  # 时间间隔
        
        self.settings = termios.tcgetattr(sys.stdin)
        
        while not rospy.is_shutdown():
            key = self.get_key()
            self.on_key_press(key)

            # 更新偏航角（平滑过渡）
            self.target_yaw = math.atan2(math.sin(self.target_yaw), math.cos(self.target_yaw))
            yaw_diff = self.target_yaw - self.current_yaw
            yaw_diff = math.atan2(math.sin(yaw_diff), math.cos(yaw_diff))
            self.current_yaw += 0.5 * yaw_diff
            self.current_yaw = math.atan2(math.sin(self.current_yaw), math.cos(self.current_yaw))
            
            # 计算运动增量
            dx = self.speed * math.cos(self.current_yaw) * dt
            dy = self.speed * math.sin(self.current_yaw) * dt
            
            # 创建并发布消息
            pose_msg = ModelState()
            pose_msg.model_name = model_name
            pose_msg.pose.position.x = self.pose.position.x + dx
            pose_msg.pose.position.y = self.pose.position.y + dy
            pose_msg.pose.position.z = self.pose.position.z
            
            # 设置朝向
            quat = quaternion_from_euler(self.current_roll, self.current_pitch, self.current_yaw)
            pose_msg.pose.orientation.x = quat[0]
            pose_msg.pose.orientation.y = quat[1]
            pose_msg.pose.orientation.z = quat[2]
            pose_msg.pose.orientation.w = quat[3]
            
            self.pos_pub.publish(pose_msg)

            # 退出控制
            if key == '\x03':  # Ctrl+C
                break

            # 有输入时打印状态
            if key != '':
                status = f"Speed: {self.speed:.2f} m/s | "
                status += f"Yaw: {math.degrees(self.current_yaw):.1f}°"
                rospy.loginfo(status)
            
            rate.sleep()

if __name__ == '__main__':
    try:
        controller = CarController()
        controller.control_loop()
    except rospy.ROSInterruptException:
        pass
