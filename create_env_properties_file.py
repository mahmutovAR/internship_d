import platform
from os.path import join as os_path_join


def main():
    """Creates file with main information about the environment
        in which the tests were executed."""
    env_data = [f'os_platform = {platform.system()}\n',
                f'os_release = {platform.release()}\n',
                f'python_version = {platform.python_version()}']

    with open(os_path_join('allure-results', 'environment.properties'), 'w') as env_file:
        for line in env_data:
            env_file.write(line)


if __name__ == '__main__':
    main()
