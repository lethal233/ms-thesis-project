# this script is aiming at processing the files downloaded from Autoware Evaluator
import yaml
import zipfile
import os

target_folder = r"C:\Users\Lori-\Downloads\scenarios\transform"


def unzip_files(zip_path: str, folder_name):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            # Build the file path
            filename = os.path.basename(member)
            # Skip directories
            if not filename:
                continue

            # Extract each file to a directory
            source = zip_ref.open(member)
            if not os.path.exists(fr"{target_folder}\{folder_name}"):
                os.makedirs(fr"{target_folder}\{folder_name}")
            target = open(os.path.join(fr"{target_folder}\{folder_name}", filename), "wb")
            with source, target:
                target.write(source.read())


def yml_file_path(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".yml") or filename.endswith(".yaml"):
            return os.path.join(directory, filename)


def unzip_maps(directory, folder_name):
    for filename in os.listdir(directory):
        if filename.endswith(".zip"):
            unzip_files(os.path.join(directory, filename), folder_name)


def read_yaml(file_name: str):
    with open(file_name, 'r') as fp:
        try:
            data = yaml.safe_load(fp)
        except yaml.YAMLError as exc:
            print(exc)
    return data


def remove_files(directory):
    for filename in os.listdir(directory):
        if not filename == 'transform':
            os.remove(os.path.join(directory, filename))


if __name__ == '__main__':
    dt = read_yaml(yml_file_path(r"C:\Users\Lori-\Downloads\scenarios"))
    folder_name = dt['OpenSCENARIO']['RoadNetwork']['LogicFile']['filepath'].split('/')[-1].split('.')[0].replace(" ",
                                                                                                                  "_").replace("(", "").replace(")", "")
    unzip_maps(r"C:\Users\Lori-\Downloads\scenarios", folder_name)
    dt['OpenSCENARIO']['RoadNetwork']['LogicFile'][
        'filepath'] = f'/home/sora/Desktop/shilonl/autoware/autoware_map/{folder_name}/lanelet2_map.osm'
    dt['OpenSCENARIO']['RoadNetwork']['SceneGraphFile'][
        'filepath'] = f'/home/sora/Desktop/shilonl/autoware/autoware_map/{folder_name}/pointcloud.pcd'
    with open(rf'{target_folder}\{folder_name}.yml', 'w') as file:
        yaml.dump(dt, file, default_flow_style=False)

    remove_files(r"C:\Users\Lori-\Downloads\scenarios")