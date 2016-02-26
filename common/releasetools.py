import common
import fnmatch

def InstallBoot(info):
    # Install boot files
    for filename in fnmatch.filter(info.input_zip.namelist(), "BOOT_PARTITION/*"):
        fobj = info.input_zip.read(filename)
        common.ZipWriteStr(info.output_zip, filename, fobj)
    info.script.Mount("/boot")
    info.script.UnpackPackageDir("BOOT_PARTITION", "/boot")

def InstallDebian(info):
    for filename in fnmatch.filter(info.input_zip.namelist(), "DEBIAN/*"):
        fobj = info.input_zip.read(filename)
        common.ZipWriteStr(info.output_zip, filename, fobj)
    info.script.Mount("/debian")
    info.script.UnpackPackageDir("DEBIAN", "/debian")


def FullOTA_InstallEnd(info):
    InstallBoot(info)
    InstallDebian(info)
