import sqlite3
from rosidl_runtime_py.utilities import get_message
from rclpy.serialization import deserialize_message
import json
import numpy
import argparse


class BagFileParser():
    def __init__(self, bag_file):
        self.bag_file = bag_file
        self.conn = sqlite3.connect(bag_file)
        self.cursor = self.conn.cursor()

        ## create a message type map
        topics_data = self.cursor.execute("SELECT id, name, type FROM topics").fetchall()
        self.topic_type = {name_of: type_of for id_of, name_of, type_of in topics_data}
        self.topic_id = {name_of: id_of for id_of, name_of, type_of in topics_data}
        self.topic_msg_message = {name_of: get_message(type_of) for id_of, name_of, type_of in topics_data}
        self.output_dir = "/".join(bag_file.split('/')[:-1])

    def __del__(self):
        self.conn.close()

    def get_messages(self, topic_name):
        topic_id = self.topic_id[topic_name]
        rows = self.cursor.execute(
            "SELECT timestamp, data FROM messages WHERE topic_id = {}".format(topic_id)).fetchall()
        # Deserialize all and timestamp them
        return [{"timestamp": timestamp, "msg": deserialize_message(data, self.topic_msg_message[topic_name])} for
                timestamp, data in rows]

    def output_trajectory_json(self):
        output_file: str = f"{self.output_dir}/trajectory_msg.json"
        msg: list = self.get_messages("/planning/scenario_planning/trajectory")
        traj = to_serializable(msg)
        fp = open(output_file, 'w+')
        json.dump(traj, fp, indent=4)

    def output_localization_json(self):
        output_file: str = f"{self.output_dir}/localization_msg.json"
        msg: list = self.get_messages("/localization/kinematic_state")
        locl = to_serializable(msg)
        fp = open(output_file, 'w+')
        json.dump(locl, fp, indent=4)


def to_serializable(obj):
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    elif isinstance(obj, (list, tuple)):
        return [to_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, numpy.ndarray):
        return obj.tolist()
    else:
        field_type = obj.get_fields_and_field_types()
        data = {}
        for k, v in field_type.items():
            data[k] = to_serializable(obj.__getattribute__(k))
        return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse a ROS2 bag file and extract data to JSON.')

    # Add an argument for the bag file path
    parser.add_argument('bag_file', type=str, help='The path to the ROS2 bag file.')

    # Parse the command line arguments
    args = parser.parse_args()

    # Use the parsed argument
    bag_file = args.bag_file

    parser = BagFileParser(bag_file)
    parser.output_localization_json()
    parser.output_trajectory_json()

    # trajectory: list = parser.get_messages("/planning/scenario_planning/trajectory")
    # trajectory: list = parser.get_messages("/localization/kinematic_state")
    # print((trajectory[0]['msg']))
    # sys.exit(0)
    # ddd=  to_serializable(trajectory)
    # fp = open("./scenario_rec/ces2024_wo_obs_1/localization.json", 'w+')
    # print(type(trajectory)) # list
    # print(type(trajectory[0])) # dict
    # print(trajectory[0]) # {"timestamp": xx, "msg": }
    # print(type(trajectory[0]['msg'])) # autoware_auto_planning_msgs.msg._trajectory.Trajectory
    # print(trajectory[0]['msg'])
    # print(ddd)
    # json.dump(ddd, fp, indent=4)
    # print((trajectory[0][1].header))
    # print(trajectory[0][1].header.stamp.get_fields_and_field_types())
    # print(trajectory[0][1].header.stamp.__dir__())
    # trajectory[0] tuple (int<timestamp>, trajectory_points)
    # trajectory[0][1].points trajectory_points
