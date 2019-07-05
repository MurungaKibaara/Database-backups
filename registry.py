import winreg

REG_PATH = r"SOFTWARE\smartbackups\settings"

def set_reg(name, values):
    values = values[:]
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, 
                                       winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_MULTI_SZ, values)
        winreg.CloseKey(registry_key)

        print('successfully created %s as %s in : %s\n'%(name, values, REG_PATH))
        return True

    except WindowsError:
        return False

def get_reg(name):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                       winreg.KEY_READ)
        values, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return values

    except WindowsError as error:
        print(name, 'not found : ', error)
        return None
