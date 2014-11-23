#!/usr/bin/env python
from fabric.api import task, run, abort, sudo
from fabric.operations import put, prompt
from fabric.colors import green, yellow, red
from fabric.contrib.files import upload_template, exists
from fabric.context_managers import cd

def look_for(s="", cmd=""):
    """Run cmd, ensure s in output"""
    output = run(cmd)
    if not s in output:
        abort(red("%s not in `%s`.") % (s, cmd))
    else:
        print green("%s found in `%s`." % (s, cmd))

def is_installed(what):
    """Crude determination of whether 'what' is installed on the PATH."""
    output = run("which " + what, warn_only=True, quiet=True)
    if what in output:
        return True
    return False

@task
def check_wifi():
    """
    See http://www.savagehomeautomation.com/projects/raspberry-pi-installing-the-edimax-ew-7811un-usb-wifi-adapte.html
    Check that device is recognised, kernel driver is loaded, Edimax is ready.
    """
    look_for('Edimax', cmd="lsusb")
    look_for('8192cu', cmd="lsmod")
    look_for('wlan0',  cmd="iwconfig")
    return True

@task
def configure_wifi():
    if not check_wifi:
        abort("check_wifi failed")

    ssid = prompt("Enter ssid", default="Anfield")
    pwd  = prompt("Enter WPA key")

    # see http://www.raspberrypi.org/forums/viewtopic.php?f=91&t=31003
    upload_template(
        "templates/etc_network_interfaces",
        "/etc/network/interfaces",
        use_sudo=True,
        context={"ssid":ssid, "wpa_key":pwd}
    )
    # upload_template(
    #     "templates/etc_wpa_supplicant",
    #     "/etc/wpa_supplicant/wpa_supplicant.conf",
    #     use_sudo=True, mode=0600,
    #     context={"ssid":ssid, "wpa_key":pwd}
    # )
    sudo("ifdown wlan0")
    sudo("ifup wlan0")

@task
def set_up(skip_apt=False):
    if not skip_apt:
        sudo("apt-get update")
        sudo("apt-get install supervisor authbind")

    if not is_installed("node"):
        put("scripts/install-nodejs.sh", "/tmp/install-nodejs.sh")
        sudo("/bin/sh /tmp/install-nodejs.sh")

    if not is_installed("bower"):
        sudo("npm install -g bower")

    # Configure supervisor.d
    put("templates/supervisor_conf", "/etc/supervisor/conf.d/nitelite.conf", use_sudo=True)

    # Allow 'nobody' to use port 80
    sudo("touch                /etc/authbind/byport/80")
    sudo("chown nobody:root    /etc/authbind/byport/80")
    sudo("chmod 750            /etc/authbind/byport/80")

    


@task
def is_available(what):
    print is_installed(what)

@task
def deploy(skip_install=False):
    with cd("/home/pi"):
        if exists("nitelite"):
            run("cd nitelite; git reset --hard; git pull")
        else:
            run("git clone https://github.com/mozz100/nitelite.git")
        
        with cd("nitelite/express-app"):
            if not skip_install:
                run("npm install")
                run("bower install -s")

    sudo("/etc/init.d/supervisor restart")

