import glob
import os
import time

import notify2


class BatteryNotifierError(Exception):
    pass


class BatteryNotifier:
    def __init__(self):
        if (
            not notify2.init('Battery is low')
            or not notify2.init('Battery is very low')
        ):
            raise BatteryNotifierError('Cannot init battery notifier')

        self.low = notify2.Notification(
            'Battery is low',
            'Beware your battery is low!',
            'data/images/battery-low.png',
        )
        self.very_low = notify2.Notification(
            'Battery is very low',
            'Beware your computer is about to shutdown !',
            'data/images/battery-missing.png',
        )
        self.battery_path = glob.glob('/sys/class/power_supply/BAT*')[0]

    def run(self):
        update_low = True
        update_very_low = True

        while True:
            if self.battery_charging:
                update_low = True
                update_very_low = True

            if not update_very_low:
                continue

            if not self.battery_charging and self.battery_level <= 20 and update_low:
                self.low.show()
                update_low = False

            if not self.battery_charging and self.battery_level <= 8:
                self.very_low.show()
                update_very_low = False

            time.sleep(.5)

    @property
    def battery_charging(self):
        path = os.path.join(self.battery_path, 'status')

        if not os.path.exists(path):
            raise BatteryNotifierError('Cannot find status info.')

        with open(path) as capacity_info:
            return capacity_info.read(64).rstrip() == 'Charging'

    @property
    def battery_level(self):
        path = os.path.join(self.battery_path, 'capacity')

        if not os.path.exists(path):
            raise BatteryNotifierError('Cannot find capacity info.')

        with open(path) as capacity_info:
            return int(capacity_info.read(64))


if __name__ == '__main__':
    battery_notifier = BatteryNotifier()
    battery_notifier.run()
