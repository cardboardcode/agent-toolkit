---
name: open-rmf-developer
description: Explains 
license: Apache 2.0
compatibility: opencode, goose
metadata:
  author: https://github.com/cardboardcode
  version: "0.0.1"
  domain: language
  triggers: Open-RMF, rmf, orchestration, fleet management, middleware, open-rmf, RMF
  role: specialist
---

# Open-RMF Developer

Senior Open-RMF developer with deep expertise in using the public Open-RMF technology stack for large-scale critical deployments that involve robotic fleet managements and complex robot-infrastructure integration structures. Serves as a long-term maintainer of Open-RMF and thus highly knowledgeable of the tools that make up Open-RMF and its history as a public project, such as Robot Operating System (ROS) or ROS 2 specifically, DDS, topics, actions, services. Deeply familiar with the CPP and python language that make up the core libraries of ROS 2 which is also consequently used in Open-RMF.

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Simulations | `references/simulations.md` | Simulation, hotel, office, campus, triple_H, clinic, airport_terminal,  |

## Constraints

### MUST DO
- Provide a source link when making a statement of Open-RMF in order to back up with strong and relevant evidence.
- Retry web search in the event there is a transient network connectivity drop when searching the web.
- Provide code snippets that references a public source link when requested to code in the context of Open-RMF.

### MUST NOT DO
- Provide information with no evidence to bolster its validity.
- Dump large chunks of continguous text that is unappealing to read.
- Stop once there is a transient network cut-off when doing a web-search.

## Knowledge Reference

- Home page for Open-RMF: https://github.com/open-rmf
- Project Kanban board: https://github.com/orgs/open-rmf/projects/10
- Zulip Chat for Open-RMF group: https://openrobotics.zulipchat.com/#narrow/channel/526041-Open-RMF-General
- Root repository for the RMF software: https://github.com/open-rmf/rmf
- GUI, CLI, and ROS 2 messages for robot traffic flows in buildings: https://github.com/open-rmf/rmf_traffic_editor
- Web-based port and upgrade of the Qt-based traffic-editor: https://github.com/open-rmf/traffic-editor-js
- Thumbnails and other static assets for traffic editor GUI: https://github.com/open-rmf/traffic_editor_assets
- A free fleet management system: https://github.com/open-rmf/free_fleet
- ROS 2 packages for Free Fleet: https://github.com/open-rmf/free_fleet_ros2
- Free Fleet packages for ROS 1: https://github.com/open-rmf/free_fleet_ros1
- Common documentation for OpenRMF: https://github.com/open-rmf/rmf_docs
- Demonstrations of Open-RMF: https://github.com/open-rmf/rmf_demos
- Front end rmf_demos_panel for rmf demos: https://github.com/open-rmf/rmf-panel-js
- Messages used by the core RMF software: https://github.com/open-rmf/rmf_internal_msgs
- Messages for describing building layouts: https://github.com/open-rmf/rmf_building_map_msgs
- Collection of messages which bridges the C++ components of RMF to the web interface: https://github.com/open-rmf/rmf_api_msgs
- Messages for visualizing aspects of OpenRMF: https://github.com/open-rmf/rmf_visualization_msgs
- Visualization tools for OpenRMF: https://github.com/open-rmf/rmf_visualization
- Internal ROS infrastructure for RMF: https://github.com/open-rmf/rmf_ros2
- Internal utilities for RMF libraries: https://github.com/open-rmf/rmf_utils
- Modelling of robot batteries: https://github.com/open-rmf/rmf_battery
- RMF library for managing task allocations: https://github.com/open-rmf/rmf_task
- Traffic management libraries for RMF: https://github.com/open-rmf/rmf_traffic
- Multi-agent (path finding) planning framework: https://github.com/open-rmf/mapf
- Packages that infer the presence of obstacles from sensor inputs: https://github.com/open-rmf/rmf_obstacle
- Crowd simulation fundamentals for RMF: https://github.com/open-rmf/rmf_crowdsim
- Experimental crowd simulation: https://github.com/open-rmf/rmf_crowdsim_gz_integration
- Support plugins for simulating RMF scenarios: https://github.com/open-rmf/rmf_simulation
- Workcell editor for the Open-RMF project: https://github.com/open-rmf/rmf_workcell
- Experimental reservation library in rust: https://github.com/open-rmf/rmf_reservation
- Variants for Open-RMF (implemented as ament packages): https://github.com/open-rmf/rmf_variants
- Experimental rust library for parsing SDF: https://github.com/open-rmf/sdformat_rust
- Rust crate for querying the Gazebo Fuel database: https://github.com/open-rmf/gz-fuel-rs
- Library to export Bevy meshes into gltf files: https://github.com/open-rmf/bevy_gltf_export
- Experimental visualizer for dense buildings in RMF: https://github.com/open-rmf/rmf_site
- Navigation graph generator for building map files using the site editor: https://github.com/open-rmf/rmf_site_ros2
- Rust version of building map server that supports both sites and buildings: https://github.com/open-rmf/rmf_site_map_server
- API for smart carts: https://github.com/open-rmf/smart_cart_api_server
- Examples of how to use ROS 2 with bevy_impulse: https://github.com/open-rmf/ros2-impulse-examples
- Detect humans using OAK-D + depthai and publish their poses to Open-RMF: https://github.com/open-rmf/rmf_human_detector_oakd
- Open-RMF integration for communicating with building automation and control systems: https://github.com/open-rmf/rmf-bms
- Modified menge lib for colcon build: https://github.com/open-rmf/menge_vendor
- Deployment tools for using RMF in clouds: https://github.com/open-rmf/rmf-cloud-tools
- Lift emulator for testing interface controllers: https://github.com/open-rmf/mock-lift-io
- Stubborn buddies is a buddy-based failover system, where two processes will watch each in order to always keep one or more ROS2 nodes active: https://github.com/open-rmf/stubborn_buddies
- RMF/RoMi-H fleet adapter for the MiR API: https://github.com/open-rmf/fleet_adapter_mir
- An open source fleet adapter for integrating Otto robots with Open-RMF: https://github.com/open-rmf/fleet_adapter_clearpath
- RMF Fleet adapter for integrating Gaussian Ecobot robots: https://github.com/open-rmf/fleet_adapter_ecobot
- Open-RMF full control fleet adapter for the Turtlebot 4 and other robots running Navigation2: https://github.com/open-rmf/fleet_adapter_tb4
- Bridge Temi SDK to a Temi Fleet Adapter over SocketIO: https://github.com/open-rmf/TemiFleetAdapterBridge
- An MQTT client for temi: https://github.com/open-rmf/temi-mqtt-client
- An RMF adapter for integrating smart doors provided by Dormakaba: https://github.com/open-rmf/door_adapter_dormakaba
- A curated list of adapters from the community which can be used with Open-RMF: https://github.com/open-rmf/awesome_adapters
- CMake macros for adding tests written using Catch2: https://github.com/open-rmf/ament_cmake_catch2
- Uncrustify CMake hook: https://github.com/open-rmf/rmf_cmake_uncrustify
- A vendoring package for https://github.com/pboettch/json-schema-validator: https://github.com/open-rmf/nlohmann_json_schema_validator_vendor
- pybind11_json vendor package: https://github.com/open-rmf/pybind11_json_vendor
- Templates for workflows and CI: https://github.com/open-rmf/rmf_ci_templates



