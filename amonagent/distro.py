import wmi
import platform

def windows_platform_data():
    platform_data = {}
    wmi_c = wmi.WMI()
    # http://msdn.microsoft.com/en-us/library/windows/desktop/aa394102%28v=vs.85%29.aspx
    # systeminfo = wmi_c.Win32_ComputerSystem()[0]
    # http://msdn.microsoft.com/en-us/library/windows/desktop/aa394239%28v=vs.85%29.aspx
    osinfo = wmi_c.Win32_OperatingSystem()[0]

    platform_data['processor'] = {
        'modelname': platform.processor()
    }
    
    (osfullname, _) = osinfo.Name.split('|', 1)
    osfullname = osfullname.strip()

    platform_data['distro'] = {
        'version': osfullname,
        'name': 'windows'
    }

    return platform_data