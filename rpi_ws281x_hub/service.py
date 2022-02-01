import click
from appdirs import user_config_dir
from os import path, makedirs
from shutil import copyfile

service_name = 'rpi-ws281x-hub'
config_dir = user_config_dir(service_name)
install_dir = '/lib/systemd/system'
module_dir = path.dirname(__file__)

def docstring_parameter(*args, **kwargs):
    def decorator(obj):
        obj.__doc__ = obj.__doc__.format(*args, **kwargs)
        return obj
    return decorator

@click.command()
@click.argument('action')
@docstring_parameter(service_name=service_name)
def cli(action):
    """
    {service_name} service managment cli

    ACTIONS : 
    
    * install (install service file)
    """
    if action == 'install':
        service_filename = f'{service_name}.service'
        service_file = path.join(module_dir, service_filename)
        installed_service_file = path.join(install_dir, service_filename)
        print(f'🔧 installing {installed_service_file} ...')
        if not path.exists(installed_service_file):
            copyfile(service_file, installed_service_file)
    else:
        print('unknown action')

if __name__ == "__main__":
    cli()