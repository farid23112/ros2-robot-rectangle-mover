# ROS 2 Robot Rectangle Mover

Package ROS 2 untuk menggerakkan robot differential-drive pada simulasi Gazebo mengikuti lintasan persegi panjang 4 m × 2 m.

## Node
- `mover_node`: contoh gerak dasar.
- `rectangle_mover`: lintasan persegi panjang.

## Topic
- `/cmd_vel`: perintah kecepatan robot.
- `/joint_states`: posisi joint roda.

## Parameter
- Radius roda: 0,1 m
- Jarak antar roda: 0,45 m
- Panjang lintasan: 4 m
- Lebar lintasan: 2 m
- Kecepatan linear: 0,3 m/s
- Kecepatan angular: 0,3 rad/s

## Build

```bash
cd ~/ros2_ws
colcon build --packages-select simple_mover
source install/setup.bash
```

## Menjalankan

Jalankan simulasi robot:

```bash
ros2 launch robin_bringup my_robot_gazebo.launch.py
```

Pada terminal lain:

```bash
cd ~/ros2_ws
source install/setup.bash
ros2 run simple_mover rectangle_mover
```

## Alur lintasan

4 m → 90° → 2 m → 90° → 4 m → 90° → 2 m → 90° → berhenti.

## Catatan

Parameter robot disesuaikan dengan model simulasi yang digunakan.
