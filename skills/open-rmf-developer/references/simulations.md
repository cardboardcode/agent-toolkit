# Open-RMF Simulations

Available Gazebo simulation worlds in [`rmf_demos_gz/launch`](https://github.com/open-rmf/rmf_demos/tree/main/rmf_demos_gz/launch). All use Gazebo (GZ) with ROS 2; launch via `ros2 launch rmf_demos_gz <name>.launch.xml`.

| Launch file | World | Description |
|---|---|---|
| `hotel.launch.xml` | Hotel | Lobby + 2 guest levels; two lifts, multiple doors, 3 robot fleets (4 robots). Multi-level, multi-fleet integration. Supports `enable_experimental_lift_watchdog:=1`. |
| `office.launch.xml` | Office | Indoor office with beverage dispensing station, controllable doors, and laneways integrated into RMF. Supports DDS-Security (secure mode). |
| `airport_terminal.launch.xml` | Airport Terminal | Large-scale map with many lanes, destinations, robots, and mixed fleets. Supports crowd simulation (`use_crowdsim:=1`) and `read_only` vehicles (teleoperated caddy via `airport_terminal_caddy.launch.xml`). |
| `clinic.launch.xml` | Clinic | Two-level clinic with two lifts; two robot fleets with different roles navigating across levels. |
| `campus.launch.xml` | Campus | Planet-scale campus map using GPS WGS84 coordinates; multiple delivery robots streaming WGS84 locations. Supports RobotManager integration via MQTT bridge. |
| `triple_H.launch.xml` | Triple-H | `traffic_light` fleet scenario (pause/resume-only fleet control). Pair with `ros2 launch rmf_demos the_pedigree.launch.xml`. |
| `battle_royale.launch.xml` | Battle Royale | Multi-robot "battle" scenario with `traffic_light` (mock) fleet. Pair with `ros2 launch rmf_demos battle_go.launch.xml`. |
| `office_mock_traffic_light.launch.xml` | Office (traffic light) | Office world with `tinyRobot2` as a `traffic_light` robot (vs full-control `tinyRobot1`). Pair with `ros2 launch rmf_demos office_traffic_light_test.launch.xml`. |
| `simulation.launch.xml` | (any map) | Generic world launcher: `ros2 launch rmf_demos_gz simulation.launch.xml map_name:=<map> [use_crowdsim:=1] [headless:=1]`. Available maps in `rmf_demos_maps`: hotel, office, airport_terminal, clinic, campus, triple_H, battle_royale. |

## Notes

- Common launch arguments: `headless` (default `1`, use `headless:=0` for GUI), `use_crowdsim` (Menge crowd simulation, default `0`), `map_package` (default `rmf_demos_maps`).
- Task dispatching via CLI: `ros2 run rmf_demos_tasks dispatch_patrol|dispatch_delivery|dispatch_clean ... --use_sim_time` (see `rmf_demos_tasks/README.md`).
- Emergency alarm feature: `ros2 topic pub -1 /fire_alarm_trigger std_msgs/Bool '{data: true}'` directs all robots to nearest parking spot.
- Reference: https://github.com/open-rmf/rmf_demos
