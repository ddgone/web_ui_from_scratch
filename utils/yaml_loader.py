import yaml


def load_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def get_test_data(file_path, case_name):
    data = load_yaml(file_path)
    for case in data:
        if case.get('case_name') == case_name:
            return case.get('test_data')
    return None


if __name__ == '__main__':
    yaml_file_path = "../data/case_yaml/baidu_homepage_data.yaml"
    test_case_name = "test_baidu_search"
    content = get_test_data(yaml_file_path, test_case_name)
    print(content)
