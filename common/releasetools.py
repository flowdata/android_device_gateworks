import common
import fnmatch

def InstallBoot(info):
    # Install boot files
    for filename in fnmatch.filter(info.input_zip.namelist(), "BOOT_EXTRA/*"):
        fobj = info.input_zip.read(filename)
        common.ZipWriteStr(info.output_zip, filename, fobj)
    info.script.Mount("/boot")
    info.script.UnpackPackageDir("BOOT_EXTRA", "/boot")
    info.script.AppendExtra('package_extract_file("boot.img", "/boot/boot.img");')

def FullOTA_InstallEnd(info):
    InstallBoot(info)
