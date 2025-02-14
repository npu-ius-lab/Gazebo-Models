# 适用于Gazebo仿真的模型与世界文件

本仓库收集了适用于Gazebo仿真的诸多模型文件，包括场景、物件、载具、世界文件等。主要应用于PX4与Gazebo的联合仿真。
>如果你只是使用Gazebo，或者使用的是其他与Gazebo联动的软件包，自行为Gazebo配置环境变量即可。

在Ubuntu 20.04 + Gazebo 11下验证通过。
___

## [ 声明 ]

本仓库的模型来源为[3DGEMS](https://data.nvision2.eecs.yorku.ca/3DGEMS/), [PX4 Gazebo Plugin Suite](https://github.com/PX4/PX4-SITL_gazebo-classic/tree/main)与[Realsense_Ros_Gazebo](https://gitee.com/nie_xun/realsense_ros_gazebo)。

- **3DGEMS**
是一个包含 270 多个 3D 模型，用于在 Gazebo 仿真中进行机器人应用的数据集。但是，在数据集官网下载的模型大多有问题（模型文件中的名称标签不符合XML语法，比如包含了空格），导致无法直接调用或报错。本仓库已经基本修复了这些错误。

- **PX4 Gazebo Plugin Suite**
已经被原生集成到了PX4-Autopilot固件中，因此编译时会直接生成相关文件。但是为了应用的方便，本仓库将这些自带的模型与第三方的模型进行了分类与集成，便于查看和调用。

- **Realsense_Ros_Gazebo**
此项目源于Intel Realsense实感相机为Gazebo开发的插件，此项目的作者将官方的xacro模型文件导出为了sdf文件，并给出了配置深度相机仿真的[相关教程](https://blog.csdn.net/weixin_41469272/article/details/117919845)（虽然应用了这位作者的模型，但我不建议参照他的教程进行配置，比较麻烦且略显凌乱。我会在下面说明如何配置Realsense相机，如D435i）。

## [ 简介 ]

本仓库涵盖了大部分仿真场景，且已完成了四旋翼无人机在室内外场景利用双目深度相机D435i进行定位与规划的仿真实验。你也可以根据自己的需要编辑模型文件与世界文件进行仿真。

涵盖的模型种类如下：

- Cameras：相机：单目、双目、深度相机等。
- Decoration：装饰：相框、灯具、钟表、花瓶等。
- Earthquake：地震：模拟废墟环境的物体，如破碎的花瓶、餐具和碎片。
- Electronics：电子设备：如计算机、笔记本电脑等电子设备型号。
- Environments：环境：地板、房间、户外场景等。
- Experiment：实验：用于载具实验的道具，如标靶，棋盘格等。
- Food：食品：各种食品，如汽水瓶、糖果和甜甜圈。
- Furniture：家具：沙发、桌子、书桌、椅子等。
- Kitchen：厨房：杯子、盘子和瓶子。
- Miscellaneous：杂项：人物、地板、植物、垃圾桶等。
- Outdoors：户外：户外建筑、道路、装饰等。
- Robots：机器人：不同型号的机器人及其关节。
- Sensors：传感器：GPS、雷达、声呐等传感器。
- Shapes：形状：不同颜色的圆柱、立方体和球体等。
- Stationery：文具：包括钢笔、书籍和文件。
- Tools：工具：工具箱、锤子和锥形桶等。
- Traffic：交通：车辆模型、桥梁等。
- Vehicles：载具：可以控制并仿真的模型，如无人机、无人船、无人车等。

除`Vehicles`以外，其他模型一般都作为场景内的装饰。

世界文件`.world`本质上是调用模型和贴图组合场景而得的，你也可以用以上模型组成自己的世界文件并导出。本仓库也预设了很多世界文件以供使用。

## [ 前提条件 ]

请确保已经完成了PX4固件的编译与ROS、MAVROS的安装，并能够在gazebo中生成无人机模型。具体说来，如果你能够启动`roslaunch px4 mavros_posix_sitl.launch`，则环境正常。

如果还没有配置好PX4编译环境，请参照[Ubuntu20.04+ROS1+PX4+Gazebo仿真（三）环境配置](https://www.bilibili.com/opus/934654041226477571)和[PX4从放弃到精通（二）：ubuntu18.04配置px4编译环境及mavros环境](https://blog.csdn.net/qq_38768959/article/details/106041494?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522167361309116782425683823%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=167361309116782425683823&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_ecpm_v1~rank_v31_ecpm-4-106041494-null-null.blog_rank_default&utm_term=gazebo&spm=1018.2226.3001.4450)两篇教程进行配置。

gazebo需要使用显卡驱动，否则在加载大型场景和相机插件时会很卡。请按照[Gazebo贼卡，使用GPU加速重装显卡驱动无效解决方法](https://blog.csdn.net/weixin_63843256/article/details/145191913)和[Gazebo GPU加速【gzserver running in GPU】](https://blog.csdn.net/qq_38853759/article/details/132522471)等教程配置。

## [ 使用方法 ]

执行删除和覆盖操作之前，**最好先备份**！

**1**. 下载本仓库到任一文件夹：
```
git clone https://gitee.com/Invocatory_Weiyang/gazebo-models.git
```

**2**. 将本仓库`models`和`worlds`文件夹覆盖到`PX4-Autopilot/Tools/sitl_gazebo`下的同名文件夹。需要先删除原有的文件夹，然后再将本仓库中的同名文件夹粘贴进去。不能直接合并，有可能报错。

**3**. 用本仓库中的`CMakeLists.txt`替换掉`PX4-Autopilot/Tools/sitl_gazebo`中的同名文件。

**4**. 将本仓库中的`setup_models.bash`复制到`PX4-Autopilot/Tools/sitl_gazebo`中。
>除非你了解环境变量的配置方法，否则不要移动这个文件的位置。

**5**. 打开`PX4-Autopilot/Tools/setup_gazebo.bash`，找到这一行：
```
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:${SRC_DIR}/Tools/sitl_gazebo/models
```
在下面添加：
```
source ${SRC_DIR}/Tools/sitl_gazebo/setup_models.bash
```

**6**. 将`libgazebo_ros_openni_kinect.so`和`librealsense_gazebo_plugin.so`移动到`PX4-Autopilot/build/px4_sitl_default/build_gazebo`文件夹下。
>如果你找不到`build`文件夹，请先执行一次`make px4_sitl gazebo`命令。

**7**. 模型现在已经配置完毕，现在可以启动它了。下面将要启动一个在bayland场景中搭载前视、下视双目相机的四旋翼无人机solo进行仿真。

打开`PX4-Autopilot/launch/mavros_posix_sitl.launch`文件，找到这一段代码：
```
    <!-- vehicle model and world -->
    <arg name="est" default="ekf2"/>
    <arg name="vehicle" default="iris"/>
    <arg name="world" default="$(find mavlink_sitl_gazebo)/worlds/empty.world"/>
    <arg name="sdf" default="$(find mavlink_sitl_gazebo)/models/Vehicles/$(arg vehicle)/$(arg vehicle).sdf"/>
```
将其修改为：
```
    <!-- vehicle model and world -->
    <arg name="est" default="ekf2"/>
    <arg name="vehicle" default="solo"/>
    <arg name="my_camera" default="solo_with_frontward_downward_D435i"/>
    <arg name="world" default="$(find mavlink_sitl_gazebo)/worlds/09_baylands.world"/>
    <arg name="sdf" default="$(find mavlink_sitl_gazebo)/models/Vehicles/$(arg my_camera)/model.sdf"/>
```
然后保存退出。打开终端，执行如下命令：
```
roslaunch px4 mavros_posix_sitl.launch
```
启动时可能会报一些关于`spawn service`的错误，请耐心等待。如果过长时间仍未加载完成，可能是gazebo自动联网搜索模型了。可以尝试在`~/.bashrc`中加上：
```
export GAZEBO_MODEL_DATABASE_URI=""
```
也许有帮助。如果正确启动，应当出现了如下的场景。
![](Image1.png)

你可以新开一个终端，输入`rqt_image_view`命令，此时就能看到两个双目摄像机发送的图像数据了。

你可以将刚才更改的`launch`文件中的`my_camera`和`world`参数进行修改，改为你喜欢的机型和世界文件。我已经在`world`文件夹中预置了一些好看和实用的模型，标记为01-12，你可以选择使用。
>虽然`my_camera`参数叫这个名字，但是为它加载的模型必须是**载具模型**，而不能是单个的相机模型（换句话说，相机模型必须挂载到载具上）。
另外，不能直接替换`vehicle`的参数值来更改飞机模型，因为这个参数值是用来告诉启动文件“机型”是什么的。

## [ 已知问题 ]

本仓库尚有以下Bug未解决。

**1**. 部分模型缺失三维文件，导致无法插入。

我无法解决这个问题，因为本质上该仓库只是收集了一些模型并进行修复、验证。

**2**. Realsense双目相机同时插入两个时，只有一个在工作。

表现为不同的`image_raw`话题上发布了相同的图像。猜测是`librealsense_gazebo_plugin.so`插件的问题，但无法解决。

暂时可行的解决方法是，给另一个双目相机加载`libgazebo_ros_openni_kinect.so`插件，这样两个不同的插件独立工作，问题解决。但此插件不能发布双目话题，只有深度话题，因此如果是需要两个双目图像的应用场景就不能使用了。
>你可能会发现，`depth_camera`模型加载的插件也是上面这个插件。如果你使用这个模型仿真，深度图可能会有问题，疑似是sdf写的有缺陷。推荐使用作者配置的`realsense_camera_2`。

**3**. 配置本仓库后，使用`make px4_sitl gazebo`命令加载时会报错。

表现为：
```
[Err] [InsertModelWidget.cc:403] Missing model.config for model ...
```
不影响编译通过，但用此方式打开gazebo时会加载不出任何模型。初步推断是更改路径导致的错误，但找不到解决方法。你可以使用`roslaunch`启动gazebo，没有任何影响。