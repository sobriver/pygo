"""
自动部署jar
"""
import os

# 盘古项目路径
pangu_path = r'D:\Code\pangu'
# 中台项目路径
middle_path = r'D:\Code\middle-end'


def jar(command: int):
    """
    @param: command: 1 install; 2 deploy
    """
    cmd = ''
    if command == 1:
        cmd = "mvn clean install -Dmaven.test.skip=true"
    elif command == 2:
        cmd = "mvn clean deploy -Dmaven.test.skip=true"
    else:
        return

    run_cmd(os.path.join(middle_path, r'common-util'), cmd)
    run_cmd(os.path.join(pangu_path, r'pangu\pangu-parent'), cmd)
    run_cmd(os.path.join(pangu_path, r'pangu\pangu-ms-middle-parent-api'), cmd)
    run_cmd(os.path.join(pangu_path, r'pangu\pangu-ms-parent-api'), cmd)
    run_cmd(os.path.join(middle_path, r'bbu-middle-end-component-common'), cmd)

    run_cmd_api(os.path.join(middle_path, r'bbucloud-middleend-auth'), cmd)
    run_cmd_api(os.path.join(middle_path, r'bbucloud-misc'), cmd)
    run_cmd_api(os.path.join(middle_path, r'bbu-middle-end-micro-server-base'), cmd)
    run_cmd_api(os.path.join(middle_path, r'bbu-middle-end-micro-server-device'), cmd)
    run_cmd_api(os.path.join(middle_path, r'bbu-middle-end-micro-server-pass'), cmd)

    run_cmd(os.path.join(pangu_path, r'pangu\pangu-starter'), cmd)
    run_cmd(os.path.join(pangu_path, r'pangu\pangu-ms-middle-parent-provider'), cmd)

    run_cmd_provider(os.path.join(middle_path, r'bbucloud-middleend-auth'), cmd)
    run_cmd_provider(os.path.join(middle_path, r'bbucloud-misc'), cmd)
    run_cmd_provider(os.path.join(middle_path, r'bbu-middle-end-micro-server-base'), cmd)
    run_cmd_provider(os.path.join(middle_path, r'bbu-middle-end-micro-server-device'), cmd)
    run_cmd_provider(os.path.join(middle_path, r'bbu-middle-end-micro-server-pass'), cmd)

    run_cmd_api(os.path.join(pangu_path, r'pangu\pangu-ms-alarm'), cmd)
    run_cmd_api(os.path.join(pangu_path, r'pangu\pangu-ms-attendance'), cmd)
    run_cmd_api(os.path.join(pangu_path, r'pangu\pangu-ms-base'), cmd)
    run_cmd_api(os.path.join(pangu_path, r'pangu\pangu-ms-pass'), cmd)
    run_cmd_api(os.path.join(pangu_path, r'pangu\pangu-ms-passrecord'), cmd)
    run_cmd_api(os.path.join(pangu_path, r'pangu\pangu-ms-person'), cmd)
    run_cmd_api(os.path.join(pangu_path, r'pangu\pangu-ms-structure'), cmd)

    run_cmd(os.path.join(pangu_path, r'pangu\pangu-ms-parent-provider'), cmd)

    run_cmd_provider(os.path.join(pangu_path, r'pangu\pangu-ms-alarm'), cmd)
    run_cmd_provider(os.path.join(pangu_path, r'pangu\pangu-ms-attendance'), cmd)
    run_cmd_provider(os.path.join(pangu_path, r'pangu\pangu-ms-base'), cmd)
    run_cmd_provider(os.path.join(pangu_path, r'pangu\pangu-ms-pass'), cmd)
    run_cmd_provider(os.path.join(pangu_path, r'pangu\pangu-ms-passrecord'), cmd)
    run_cmd_provider(os.path.join(pangu_path, r'pangu\pangu-ms-person'), cmd)
    run_cmd_provider(os.path.join(pangu_path, r'pangu\pangu-ms-structure'), cmd)

    run_cmd(os.path.join(pangu_path, r'pangu\pangu-facade-parent'), cmd)
    run_cmd(os.path.join(pangu_path, r'pangu\pangu-gateway'), cmd)

    run_cmd(os.path.join(pangu_path, r'pangu\pangu-facade-web'), cmd)
    run_cmd(os.path.join(pangu_path, r'pangu\pangu-facade-openapi'), cmd)
    run_cmd(os.path.join(pangu_path, r'pangu\pangu-facade-device'), cmd)
    run_cmd(os.path.join(pangu_path, r'pangu\pangu-liquibase'), cmd)

    if command == 1:
        run_cmd(os.path.join(pangu_path, r'pangu\pangu-allinone'), cmd)


def run_cmd_api(path, cmd):
    os.chdir(path)
    for item in os.listdir(path):
        tmp_path = os.path.join(path, item)
        if os.path.isdir(tmp_path):
            if "api" in tmp_path:
                os.chdir(tmp_path)
                os.system(cmd)


def run_cmd_provider(path, cmd):
    os.chdir(path)
    for item in os.listdir(path):
        tmp_path = os.path.join(path, item)
        if os.path.isdir(tmp_path):
            if "provider" in tmp_path:
                os.chdir(tmp_path)
                os.system(cmd)


def run_cmd(path, cmd):
    os.chdir(path)
    os.system(cmd)


def install():
    """
    mvn install
    """
    jar(1)


def deploy():
    """
    mvn deploy
    """
    jar(2)


if __name__ == '__main__':
    #install()
    deploy()
