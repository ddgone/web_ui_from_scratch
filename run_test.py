import subprocess
import os
import sys
from datetime import datetime
from config.pathconf import PROPER_ALLURE_DIR


def run_tests():
    # 定义 Allure 报告的目录
    now = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    allure_results_dir = os.path.join(PROPER_ALLURE_DIR, now, 'allure_results')
    allure_report_dir = os.path.join(PROPER_ALLURE_DIR, now, 'allure_report')

    # 确保报告目录存在
    os.makedirs(allure_results_dir, exist_ok=True)
    os.makedirs(allure_report_dir, exist_ok=True)

    # 构建命令
    pytest_cmd = f"{sys.executable} -m pytest --alluredir={allure_results_dir}"
    allure_cmd = f"allure generate {allure_results_dir} -o {allure_report_dir} --clean"

    # 运行 pytest 并生成 Allure 结果
    try:
        subprocess.run(pytest_cmd, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"执行pytest时发生错误: {e}")

    # 生成 Allure 报告
    try:
        subprocess.run(allure_cmd, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"生成Allure报告时发生错误: {e}")

    # 打开 Allure 报告
    print(f"Allure报告已生成在: {allure_report_dir}")


if __name__ == '__main__':
    run_tests()
