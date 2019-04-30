import dbus
import xml.etree.ElementTree as tree
import time

#set preferred bluetooth adapter {'hci0', 'hci1', ... }
bluetooth_adapter = 'hci0'

def get_adapter():
	global bluetooth_adapter
        return dbus.SystemBus().get_object('org.bluez', '/org/bluez/' + bluetooth_adapter)

def get_adapter_path():
	global bluetooth_adapter
	return '/org/bluez/' + bluetooth_adapter

def get_adapter_interface():
	adapter = get_adapter()
	return dbus.Interface(adapter, dbus_interface='org.bluez.Adapter1')

def get_adapter_properties():
        adapter = get_adapter()
        return dbus.Interface(adapter, dbus_interface='org.freedesktop.DBus.Properties')

def get_device_name():
        adapter = get_adapter()
        adapter_xml = dbus.Interface(adapter, dbus_interface='org.freedesktop.DBus.Introspectable').Introspect()
        for device in tree.fromstring(adapter_xml).findall('node'):
                device_name = device.get('name')
                if is_connected(device_name):
			return device_name
	return None

def get_device_interface(name):
        device = dbus.SystemBus().get_object('org.bluez', get_adapter_path() + '/' + name)
	return dbus.Interface(device, dbus_interface='org.bluez.Device1')

def get_device_properties(name):
	device = dbus.SystemBus().get_object('org.bluez', get_adapter_path() + '/' + name)
        return dbus.Interface(device, dbus_interface='org.freedesktop.DBus.Properties')

def get_player():
	device = get_device_name()
	if device != None:
		player = get_player_name(device)
		if player != None:
			return dbus.SystemBus().get_object('org.bluez', get_adapter_path() + '/' + device + '/' + player)
	return None

def is_connected(name):
	properties = get_device_properties(name)
	if properties.Get('org.bluez.Device1', 'Connected') == 1:
		return True
	else:
		return False

def get_player_name(name):
	device = dbus.SystemBus().get_object('org.bluez', get_adapter_path() + '/' + name)
        device_xml = dbus.Interface(device, dbus_interface='org.freedesktop.DBus.Introspectable').Introspect()
        for node in tree.fromstring(device_xml).findall('node'):
		if 'player' in node.get('name'):
			return node.get('name')
	return None

def get_player_interface():
	player = get_player()
	if player != None:
		return dbus.Interface(player, dbus_interface='org.bluez.MediaPlayer1')
	return None

def get_player_properties():
        player = get_player()
	if player != None:
		return dbus.Interface(player, dbus_interface='org.freedesktop.DBus.Properties')
	return None

def play():
	player = get_player_interface()
	player.Play()

def pause():
	player = get_player_interface()
	player.Pause()

def next():
        player = get_player_interface()
	player.Next()

def previous():
        player = get_player_interface()
	player.Previous()

def status():
	properties = get_player_properties()
	if properties != None:
		return str(properties.Get('org.bluez.MediaPlayer1', 'Status'))
	else:
		return 'not running'

def is_running():
	if get_player() != None:
		return True
	else:
		return False

def set_powered(value):
	adapter = get_adapter_properties()
	adapter.Set('org.bluez.Adapter1', 'Powered', value)

def set_discoverable(value):
        adapter = get_adapter_properties()
        adapter.Set('org.bluez.Adapter1', 'Discoverable', value)

def set_pairable(value):
        adapter = get_adapter_properties()
        adapter.Set('org.bluez.Adapter1', 'Pairable', value)

def start_pairing():
	disconnect_device()
	set_discoverable(True)
	set_pairable(True)
	timeout = time.time() + 30
	device_found = False
	while time.time() < timeout and device_found == False:
	        adapter = get_adapter()
        	adapter_xml = dbus.Interface(adapter, dbus_interface='org.freedesktop.DBus.Introspectable').Introspect()
        	for node in tree.fromstring(adapter_xml).findall('node'):
                	name = node.get('name')
			device = get_device_properties(name)
			paired = bool(device.Get('org.bluez.Device1', 'Paired'))
			trusted = bool(device.Get('org.bluez.Device1', 'Trusted'))
			print name + str(paired) + str(trusted)
			if paired == True and trusted == False:
				device.Set('org.bluez.Device1', 'Trusted', True)
				device_found = True
				print 'now trusted: ' + name
        set_discoverable(False)
        set_pairable(False)

def disconnect_device():
	device = get_device_name()
	if device != None:
		device_interface = get_device_interface(device)
		device_interface.Disconnect()
