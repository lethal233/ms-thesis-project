# this script is aiming at processing the files downloaded from Autoware Evaluator
import yaml

if __name__ == '__main__':
    with open("C:\\Users\\Lori-\\Downloads\\LEO-VM-00002.yml", 'r') as fp:
        try:
            print(yaml.safe_load(fp))
        except yaml.YAMLError as exc:
            print(exc)