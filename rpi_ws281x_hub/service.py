import click
from appdirs import user_config_dir
from os import path, makedirs, remove, system
from shutil import copyfile
import chevron

service_name = 'rpi-ws281x-hub'
config_dir = user_config_dir(service_name)
install_dir = '/lib/systemd/system'
module_dir = path.dirname(__file__)

def docstring_parameter(*args, **kwargs):
    def decorator(obj):
        obj.__doc__ = obj.__doc__.format(*args, **kwargs)
        return obj
    return decorator

def render_service_template(file):
    with open(file, 'r') as f:
        return chevron.render(f.read(), {
            'service_name': service_name,
            'working_directory': module_dir})

@click.command()
@click.argument('action')
@docstring_parameter(service_name=service_name)
def cli(action):
    """
    {service_name} service managment cli

    ACTIONS : 

    * install (install service file)
    """
    service_filename = f'{service_name}.service'
    service_file = path.join(module_dir, service_filename)
    installed_service_file = path.join(install_dir, service_filename)

    if action == 'render':
        print(f'✨ render {installed_service_file} ...')
        print(render_service_template(service_file))
    elif action == 'install':
        print(f'✨ installing {installed_service_file} ...')
        if not path.exists(installed_service_file):
            with open(installed_service_file, 'w') as f:
                f.write(render_service_template(service_file))
    elif action == 'uninstall':
        print(f'💀 un-installing {installed_service_file} ...')
        if path.exists(installed_service_file):
            remove(installed_service_file)
    elif action in ['enable', 'start', 'stop', 'status']:
        print(f'{action} {installed_service_file} ...')
        system(f'systemctl {action} {service_filename}')
    else:
        print('unknown action')

if __name__ == "__main__":
    cli()