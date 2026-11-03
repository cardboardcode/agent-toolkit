# Open-RMF Simulations

Available Gazebo simulation worlds in [`rmf_demos_gz/launch`](https://github.com/open-rmf/rmf_demos/tree/main/rmf_demos_gz/launch). All use Gazebo (GZ) with ROS 2; launch via `ros2 launch rmf_demos_gz <name>.launch.xml`.

Fleet/robot names come from the `rmf_fleet` fleet config YAMLs under `rmf_demos/config/`; door, lift, and floor data come from each world's `<name>.building.yaml` map definition in `rmf_demos_maps`.

| World | Fleets | Robots | Doors | Lifts | Floors | Mutex field on edges? | Actual mutex groups | `use_reservation_node` |
|---|---|---|---|---|---|---|---|---|
| Hotel | 3 (`cleanerBotA`, `tinyRobot`, `deliveryRobot`) | 4 (`cleanerBotA_1`, `cleanerBotA_2`, `tinyBot_1`, `deliveryBot_1`) | 19 (`L1_door1`–`L1_door5`; `L2_door2/5/9/11/12/14/15`; `L3_door2/5/9/11/12/14/15`) | 2 (`Lift1`, `Lift2`) | 3 (`L1`, `L2`, `L3`) | No | ❌ None | No (default `false`) |
| Office | 1 (`tinyRobot`) | 2 (`tinyRobot1`, `tinyRobot2`) | 3 (`main_door`, `coe_door`, `hardware_door`) | 0 | 1 (`L1`) | Yes — 30 edges carry the field | ❌ None (all empty) | **Yes** (`rmf_demos/launch/office.launch.xml` passes `<arg name="use_reservation_node" value="true"/>` to `common.launch.xml`) |
| Airport Terminal | 5 (`cleanerBotA`, `cleanerBotE`, `deliveryRobot`, `tinyRobot`, `caddy` read-only) | 8 (`cleanerBotA_0`, `cleanerBotE_0`, `cleanerBotE_1`, `deliveryRobot_0`, `deliveryRobot_1`, `tinyRobot_0`, `tinyRobot_1`, `caddy`) | 5 (`n01_door`, `n02_door`, `s04_door`, `s08_door`, `zone_4_door`) | 0 | 1 (`L1`) | No | ❌ None | No (default `false`) |
| Clinic | 2 (`deliveryRobot`, `tinyRobot`) | 4 (`deliveryRobot_1`, `deliveryRobot_2`, `tinyRobot_1`, `tinyRobot_2`) | 132 (L1: 76, L2: 56; e.g. `L1_clinic_a`, `L1_clinic_b`, per consultation/treatment room pairs) | 4 (`lift_1`, `lift_2`, `lift_24`, `lift_25`) | 2 (`L1`, `L2`) | No | ❌ None | No (default `false`) |
| Campus | 1 (`DeliveryRobot`) | 2 (`deliveryRobot_1`, `deliveryRobot_2`) | 0 | 0 | 1 (`L1`) | No | ❌ None | No (default `false`) |
| Triple-H | 1 (`tinyRobot`, inline traffic-light adapter) | 4 (`tinyRobotTopLeft`, `tinyRobotTopRight`, `tinyRobotBottomLeft`, `tinyRobotBottomRight`) | 0 | 0 | 1 (`L1`) | No | ❌ None | No (default `false`) |
| Battle Royale | 1 (`tinyRobot`) | 4 (`tinyRobotA`, `tinyRobotB`, `tinyRobotC`, `tinyRobotD`) | 0 | 0 | 1 (`L1`) | No | ❌ None | No (default `false`) |
| Office (traffic light) | 2 (`tinyRobot1` full-control, `tinyRobot2` mock traffic-light) | 2 (`tinyRobot1`, `tinyRobot2`) | 3 (`main_door`, `coe_door`, `hardware_door`) | 0 | 1 (`L1`) | Yes — 30 edges carry the field | ❌ None (all empty) | No (default `false`) |

### Mutex groups

**None of the simulations have mutex groups actually configured.**

- The **office** map is the only one whose edge entries even *include* the `mutex` attribute; in `office.building.yaml` **every single one** has an empty value:

  ```yaml
  - [39, 40, {..., mutex: [1, ""], ...}]
  ```

- Across all maps, there are **zero** edges with a non-empty `mutex` value (i.e. no `mutex: [1, "<group_name>"]` anywhere).
- RMF "mutex groups" are typically declared as named strings on edges/nodes (e.g. `"mutual_exclusion" / "traffic_light:..."`). I found no such named assignments.

### `use_reservation_node`

`common.launch.xml` declares `<arg name="use_reservation_node" default="false" description="Enable the reservation node for parking spot de-confliction"/>` and conditionally launches the reservation node only when the argument is `true`.

- **Office** is the *only* top-level launch file that sets it: `rmf_demos/launch/office.launch.xml` passes `<arg name="use_reservation_node" value="true"/>`. Since `rmf_demos_gz/launch/office.launch.xml` includes that file, the Gazebo office simulation also runs with the reservation node enabled.
- None of the other launch files (hotel, clinic, campus, airport_terminal, triple_H, battle_royale, office_mock_traffic_light) pass the argument, so they all use the `false` default.

### Upstream Removal of Build-Time Model Downloads to `~/.gazebo/models`

- In older distributions (`humble`, `jazzy`), `rmf_demos_maps/CMakeLists.txt` ran:
  ```cmake
  COMMAND ros2 run rmf_building_map_tools building_map_model_downloader ${map_path} -e ~/.gazebo/models
  ```
  which used `pit_crew` during `colcon build` to pre-download Fuel models into `/root/.gazebo/models`.
- On `main` (and `lyrical`/`rolling`), two upstream commits removed build-time model downloading into `~/.gazebo/models`:
  - **`open-rmf/rmf_traffic_editor` (`4e38668` — *"Download models through Gazebo (#535)"*)**: Changed `building_map_model_downloader` so it only updates the Fuel model listing cache at `/root/.pit_crew/model_cache.json` and writes `https://fuel.gazebosim.org/...` URIs into the generated `.world` SDF files for Gazebo to download on-demand at runtime.
  - **`open-rmf/rmf_demos` (`770c1a9` — *"Use builtin gazebo model downloading (#307)"*)**: Removed `-e ~/.gazebo/models` from `rmf_demos_maps/CMakeLists.txt` and changed the custom target to only invoke `ros2 run rmf_building_map_tools building_map_model_downloader`.
- Consequently, `/root/.gazebo/models` is never created during `colcon build` in `Dockerfile.latest` or `Dockerfile.rolling` (note that this `COPY` line was already removed from `Dockerfile.lyrical`).

## Knowledge Reference

- Reference: https://github.com/open-rmf/rmf_demos
