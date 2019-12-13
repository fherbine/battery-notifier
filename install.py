import os
import getpass

if __name__ == '__main__':
    os.system('pip install -r requirements.txt')
    user = getpass.getuser()
    home = os.path.join('/', 'home', user)
    install_path = os.getcwd()
    desktop_file = 'battery-notifier.desktop'

    # following part could differ depending on your version
    if not os.path.exists(os.path.join(home, '.config')):
        os.mkdir(os.path.join(home, '.config'))

    autostart_folder = os.path.join(home, '.config', 'autostart')

    if not os.path.exists(autostart_folder):
        os.mkdir(autostart_folder)
    # --------

    with open(desktop_file, 'a') as dfile:
        dfile.write('Exec=%s/start.sh' % install_path)

    os.system(f'cp {desktop_file} {autostart_folder}/')
    print('Install done!\nYou can reboot your system NOW.')
