import subprocess
import pkg_resources


def main():
    # Alembic upgrade command from where alembic.ini is located
    alembic_ini_path = pkg_resources.resource_filename('gateway', 'alembic.ini')
    alembic_upgrade_command = 'alembic upgrade head'
    subprocess.run(alembic_upgrade_command, shell=True, cwd=alembic_ini_path)


if __name__ == '__main__':
    main()
