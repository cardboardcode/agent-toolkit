# Open-RMF Simulations

Available Gazebo simulation worlds in [`rmf_demos_gz/launch`](https://github.com/open-rmf/rmf_demos/tree/main/rmf_demos_gz/launch). All use Gazebo (GZ) with ROS 2; launch via `ros2 launch rmf_demos_gz <name>.launch.xml`.

Fleet/robot names come from the `rmf_fleet` fleet config YAMLs under `rmf_demos/config/`; door, lift, and floor data come from each world's `<name>.building.yaml` map definition in `rmf_demos_maps`.

| World | Fleets | Robots | Doors | Lifts | Floors |
|---|---|---|---|---|---|
| Hotel | 3 (`cleanerBotA`, `tinyRobot`, `deliveryRobot`) | 4 (`cleanerBotA_1`, `cleanerBotA_2`, `tinyBot_1`, `deliveryBot_1`) | 19 (`L1_door1`–`L1_door5`; `L2_door2/5/9/11/12/14/15`; `L3_door2/5/9/11/12/14/15`) | 2 (`Lift1`, `Lift2`) | 3 (`L1`, `L2`, `L3`) |
| Office | 1 (`tinyRobot`) | 2 (`tinyRobot1`, `tinyRobot2`) | 3 (`main_door`, `coe_door`, `hardware_door`) | 0 | 1 (`L1`) |
| Airport Terminal | 5 (`cleanerBotA`, `cleanerBotE`, `deliveryRobot`, `tinyRobot`, `caddy` read-only) | 8 (`cleanerBotA_0`, `cleanerBotE_0`, `cleanerBotE_1`, `deliveryRobot_0`, `deliveryRobot_1`, `tinyRobot_0`, `tinyRobot_1`, `caddy`) | 5 (`n01_door`, `n02_door`, `s04_door`, `s08_door`, `zone_4_door`) | 0 | 1 (`L1`) |
| Clinic | 2 (`deliveryRobot`, `tinyRobot`) | 4 (`deliveryRobot_1`, `deliveryRobot_2`, `tinyRobot_1`, `tinyRobot_2`) | 132 (L1: 76, L2: 56; e.g. `L1_clinic_a`, `L1_clinic_b`, per consultation/treatment room pairs) | 4 (`lift_1`, `lift_2`, `lift_24`, `lift_25`) | 2 (`L1`, `L2`) |
| Campus | 1 (`DeliveryRobot`) | 2 (`deliveryRobot_1`, `deliveryRobot_2`) | 0 | 0 | 1 (`L1`) |
| Triple-H | 1 (`tinyRobot`, inline traffic-light adapter) | 4 (`tinyRobotTopLeft`, `tinyRobotTopRight`, `tinyRobotBottomLeft`, `tinyRobotBottomRight`) | 0 | 0 | 1 (`L1`) |
| Battle Royale | 1 (`tinyRobot`) | 4 (`tinyRobotA`, `tinyRobotB`, `tinyRobotC`, `tinyRobotD`) | 0 | 0 | 1 (`L1`) |
| Office (traffic light) | 2 (`tinyRobot1` full-control, `tinyRobot2` mock traffic-light) | 2 (`tinyRobot1`, `tinyRobot2`) | 3 (`main_door`, `coe_door`, `hardware_door`) | 0 | 1 (`L1`) |

## Knowledge Reference

- Reference: https://github.com/open-rmf/rmf_demos
