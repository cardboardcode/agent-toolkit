## Compatibility Matrix

Each row is an Open-RMF release line (one per supported ROS 2 distribution). Each **dependency column** lists the pinned version of that core package for the given release, taken from the `rmf.repos` manifest linked in the release notes:

- [rmf_ros2](https://github.com/open-rmf/rmf_ros2) — core ROS 2 integration (fleet adapter, task manager)
- [rmf_traffic](https://github.com/open-rmf/rmf_traffic) — traffic / path-planning + reservation
- [rmf_task](https://github.com/open-rmf/rmf_task) — task allocation & sequencing
- [rmf_demos](https://github.com/open-rmf/rmf_demos) — example fleets & Gazebo worlds (built from source)
- [rmf_internal_msgs](https://github.com/open-rmf/rmf_internal_msgs) — core message definitions
- [menge_vendor](https://github.com/open-rmf/menge_vendor) — crowd-simulation engine (third-party)

| Open-RMF Release | Link | ROS 2 / Ubuntu | Gazebo | rmf_ros2 | rmf_traffic | rmf_task | rmf_demos | rmf_internal_msgs | menge_vendor |
|---|---|---|---|---|---|---|---|---|---|
| Open-RMF on Jazzy Jalisco ([tag](https://github.com/open-rmf/rmf/blob/release-jazzy-240617/rmf.repos)) | https://github.com/open-rmf/rmf/releases/tag/release-jazzy-240617 | Jazzy / 24.04 | Harmonic | 2.7.2 | 3.3.3 | 2.5.1 | 2.3.0 | 3.3.1 | 1.2.1 |
| Open-RMF on Rolling Ridley ([tag](https://github.com/open-rmf/rmf/blob/release-rolling-231229/rmf.repos)) | https://github.com/open-rmf/rmf/releases/tag/release-rolling-231229 | Rolling / 22.04 | Harmonic | 2.5.0 | 3.3.1 | 2.4.0 | 2.2.3 | 3.2.1 | 1.2.0 |
| Open-RMF on Iron Irwini ([tag](https://github.com/open-rmf/rmf/blob/release-iron-231229/rmf.repos)) | https://github.com/open-rmf/rmf/releases/tag/release-iron-231229 | Iron / 22.04 | Garden | 2.2.5 | 3.1.2 | 2.2.4 | 2.1.2 | 3.1.1 | 1.1.1 |
| Open-RMF on Humble Hawksbill ([tag](https://github.com/open-rmf/rmf/blob/release-humble-231229/rmf.repos)) | https://github.com/open-rmf/rmf/releases/tag/release-humble-231229 | Humble / 22.04 | Fortress | 2.1.8 | 3.0.3 | 2.1.8 | 2.0.4 | 3.0.4 | 1.0.1 |

> **Notes**
> - The **Jazzy** release is the only one documented as *exclusively* supporting **Gazebo Harmonic** (using Harmonic's ECS APIs for up to ~70% better Real-Time Factor); it is the primary supported line on **Ubuntu 24.04**.
> - The Humble / Iron / Rolling pairings follow the ROS 2 recommended Gazebo release for each distro (Fortress / Garden / Harmonic).
> - `rmf_demos` is **not shipped as binaries** for any of these releases and must be built from source.

## Knowledge References

- Main GitHub Repository: https://github.com/open-rmf/rmf
- Release Page: https://github.com/open-rmf/rmf/releases
- Jazzy release `rmf.repos` (version manifest): https://github.com/open-rmf/rmf/blob/release-jazzy-240617/rmf.repos
- Open Robotics — "Open-RMF gets Jazzy" (Gazebo Harmonic, Ubuntu 24.04): https://www.openrobotics.org/blog/2024/8/18/open-rmf-gets-jazzy
- GZ ↔ ROS pairing table: https://gazebosim.org/docs/latest/ros_installation/