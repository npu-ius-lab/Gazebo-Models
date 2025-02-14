# 适用于Gazebo仿真的模型与世界文件

本仓库收集了适用于Gazebo仿真的诸多模型文件，包括场景、物件、载具、世界文件等。主要应用于PX4与Gazebo的联合仿真。
>如果你只是使用Gazebo，或者使用的是其他与Gazebo联动的软件包，自行为Gazebo配置环境变量即可。

在Ubuntu 20.04 + Gazebo 11下验证通过。
___

## [ 声明 ]

本仓库的模型来源为[3DGEMS](https://data.nvision2.eecs.yorku.ca/3DGEMS/), [PX4 Gazebo Plugin Suite](https://github.com/PX4/PX4-SITL_gazebo-classic/tree/main)与[Realsense_Ros_Gazebo](https://gitee.com/nie_xun/realsense_ros_gazebo)。

- **3DGEMS**
是一个包含 270 多个 3D 模型，用于在 Gazebo 仿真中进行机器人应用的数据集。但是，在数据集官网下载的模型大多有问题（模型文件中的名称标签不符合XML语法，比如包含了空格），导致无法直接调用或报错。本仓库已经尽量修复了这些错误。

- **PX4 Gazebo Plugin Suite**
已经被原生集成到了PX4-Autopilot固件中，因此编译时会直接生成相关文件。但是为了应用的方便，本仓库将这些自带的模型与第三方的模型进行了分类与集成，便于查看和调用。

- **Realsense_Ros_Gazebo**
此项目源于Intel Realsense实感相机为Gazebo开发的插件，此项目的作者将官方的xacro模型文件导出为了sdf文件，并给出了配置深度相机仿真的[相关教程](https://blog.csdn.net/weixin_41469272/article/details/117919845)（虽然应用了这位作者的模型，但我不建议参照他的教程进行配置，比较麻烦且略显凌乱。我会在下面说明如何配置Realsense相机，如D435i）。

本仓库涵盖了大部分仿真场景，且已完成了四旋翼无人机在室内外场景利用双目深度相机D435i进行定位与规划的仿真实验。你也可以根据自己的需要编辑模型文件与世界文件进行仿真。

## [ 前提条件 ]

请确保已经完成了PX4固件的编译，并能够在gazebo中生成无人机模型。具体说来，如果你能够在`/PX4-Autopilot`调用`make px4_sitl gazebo`命令，说明配置已经成功。

如果还没有配置好PX4编译环境，请参照[Ubuntu20.04+ROS1+PX4+Gazebo仿真（三）环境配置](https://www.bilibili.com/opus/934654041226477571)和[]()进行配置。

若使用PX4固件进行gazebo仿真，将`models`和`worlds`文件夹合并到`PX4-Autopilot/Tools/sitl_gazebo`下的同名文件夹即可。
