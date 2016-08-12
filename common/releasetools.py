#import common
#import fnmatch
#import copy
#import os
#
#def IsSymlink(info):
#  """Return true if the zipfile.ZipInfo object passed in represents a
#  symlink."""
#  return (info.external_attr >> 16) == 0120777
#
#def MostPopularKey(d, default):
#  """Given a dict, return the key corresponding to the largest
#  value.  Returns 'default' if the dict is empty."""
#  x = [(v, k) for (k, v) in d.iteritems()]
#  if not x: return default
#  x.sort()
#  return x[-1][1]
#
#
#
#class Item:
#  """Items represent the metadata (user, group, mode) of files and
#  directories in the system image."""
#  ITEMS = {}
#  def __init__(self, name, dir=False):
#    self.name = name
#    self.uid = None
#    self.gid = None
#    self.mode = None
#    self.selabel = None
#    self.capabilities = None
#    self.dir = dir
#
#    if name:
#      self.parent = Item.Get(os.path.dirname(name), dir=True)
#      self.parent.children.append(self)
#    else:
#      self.parent = None
#    if dir:
#      self.children = []
#
#  def Dump(self, indent=0):
#    if self.uid is not None:
#      print "%s%s %d %d %o" % ("  "*indent, self.name, self.uid, self.gid, self.mode)
#    else:
#      print "%s%s %s %s %s" % ("  "*indent, self.name, self.uid, self.gid, self.mode)
#    if self.dir:
#      print "%s%s" % ("  "*indent, self.descendants)
#      print "%s%s" % ("  "*indent, self.best_subtree)
#      for i in self.children:
#        i.Dump(indent=indent+1)
#
#  @classmethod
#  def Get(cls, name, dir=False):
#    if name not in cls.ITEMS:
#      cls.ITEMS[name] = Item(name, dir=dir)
#    return cls.ITEMS[name]
#
#  @classmethod
#  def GetMetadata(cls, input_zip):
#
#    # The target_files contains a record of what the uid,
#    # gid, and mode are supposed to be.
#    output = input_zip.read("META/debian_filesystem_config.txt")
#
#    for line in output.split("\n"):
#      if not line: continue
#      columns = line.split(';')
#      name, uid, gid, mode = columns[:4]
#      selabel = None
#      capabilities = None
#
#      # After the first 4 columns, there are a series of key=value
#      # pairs. Extract out the fields we care about.
#      for element in columns[4:]:
#          try:
#              key, value = element.split("=")
#              if key == "selabel":
#                  selabel = value
#              if key == "capabilities":
#                  capabilities = value
#          except:
#              print ("Failed to split value %r %r" % (element, columns))
#
#      i = cls.ITEMS.get(name, None)
#      if i is not None:
#        i.uid = int(uid)
#        i.gid = int(gid)
#        i.mode = int(mode, 8)
#        i.selabel = selabel
#        i.capabilities = capabilities
#        if i.dir:
#          i.children.sort(key=lambda i: i.name)
#
#  def CountChildMetadata(self):
#    """Count up the (uid, gid, mode, selabel, capabilities) tuples for
#    all children and determine the best strategy for using set_perm_recursive and
#    set_perm to correctly chown/chmod all the files to their desired
#    values.  Recursively calls itself for all descendants.
#
#    Returns a dict of {(uid, gid, dmode, fmode, selabel, capabilities): count} counting up
#    all descendants of this node.  (dmode or fmode may be None.)  Also
#    sets the best_subtree of each directory Item to the (uid, gid,
#    dmode, fmode, selabel, capabilities) tuple that will match the most
#    descendants of that Item.
#    """
#
#    assert self.dir
#    d = self.descendants = {(self.uid, self.gid, self.mode, None, self.selabel, self.capabilities): 1}
#    for i in self.children:
#      if i.dir:
#        for k, v in i.CountChildMetadata().iteritems():
#          d[k] = d.get(k, 0) + v
#      else:
#        k = (i.uid, i.gid, None, i.mode, i.selabel, i.capabilities)
#        d[k] = d.get(k, 0) + 1
#
#    # Find the (uid, gid, dmode, fmode, selabel, capabilities)
#    # tuple that matches the most descendants.
#
#    # First, find the (uid, gid) pair that matches the most
#    # descendants.
#    ug = {}
#    for (uid, gid, _, _, _, _), count in d.iteritems():
#      ug[(uid, gid)] = ug.get((uid, gid), 0) + count
#    ug = MostPopularKey(ug, (0, 0))
#
#    # Now find the dmode, fmode, selabel, and capabilities that match
#    # the most descendants with that (uid, gid), and choose those.
#    best_dmode = (0, 0755)
#    best_fmode = (0, 0644)
#    best_selabel = (0, None)
#    best_capabilities = (0, None)
#    for k, count in d.iteritems():
#      if k[:2] != ug: continue
#      if k[2] is not None and count >= best_dmode[0]: best_dmode = (count, k[2])
#      if k[3] is not None and count >= best_fmode[0]: best_fmode = (count, k[3])
#      if k[4] is not None and count >= best_selabel[0]: best_selabel = (count, k[4])
#      if k[5] is not None and count >= best_capabilities[0]: best_capabilities = (count, k[5])
#    self.best_subtree = ug + (best_dmode[1], best_fmode[1], best_selabel[1], best_capabilities[1])
#
#    return d
#
#  def SetPermissions(self, script):
#    """Append set_perm/set_perm_recursive commands to 'script' to
#    set all permissions, users, and groups for the tree of files
#    rooted at 'self'."""
#
#    self.CountChildMetadata()
#
#    def recurse(item, current):
#      # current is the (uid, gid, dmode, fmode, selabel, capabilities) tuple that the current
#      # item (and all its children) have already been set to.  We only
#      # need to issue set_perm/set_perm_recursive commands if we're
#      # supposed to be something different.
#      if item.dir:
#        if current != item.best_subtree:
#          script.SetPermissionsRecursive("/"+item.name, *item.best_subtree)
#          current = item.best_subtree
#
#        if item.uid != current[0] or item.gid != current[1] or \
#           item.mode != current[2] or item.selabel != current[4] or \
#           item.capabilities != current[5]:
#          script.SetPermissions("/"+item.name, item.uid, item.gid,
#                                item.mode, item.selabel, item.capabilities)
#
#        for i in item.children:
#          recurse(i, current)
#      else:
#        if item.uid != current[0] or item.gid != current[1] or \
#               item.mode != current[3] or item.selabel != current[4] or \
#               item.capabilities != current[5]:
#          try:
#              script.SetPermissions("/"+item.name, item.uid, item.gid,
#                                item.mode, item.selabel, item.capabilities)
#          except:
#              print("Couldn't set permissions for %r" % item.name)
#
#    recurse(self, (-1, -1, -1, -1, None, None))
#
#
#def CopyDebianFiles(input_zip, output_zip=None,
#                    substitute=None):
#  """Copies files underneath system/ in the input zip to the output
#  zip.  Populates the Item class with their metadata, and returns a
#  list of symlinks.  output_zip may be None, in which case the copy is
#  skipped (but the other side effects still happen).  substitute is an
#  optional dict of {output filename: contents} to be output instead of
#  certain input files.
#  """
#
#  symlinks = []
#
#  for info in input_zip.infolist():
#    if info.filename.startswith("DEBIAN/"):
#      basefilename = info.filename[7:]
#      if IsSymlink(info):
#          # Deal with the fragility of android's tools WRT ISO8859-1.
#          addline = True
#          for char in basefilename:
#              if ord(char) >= 128:
#                  addline = False
#                  break
#          if not addline:
#              continue
#          data = input_zip.read(info.filename)
#          for char in info.filename:
#              if ord(char) > 128:
#                  addline = False
#          symlinks.append((data, "/debian/" + basefilename))
#      else:
#        info2 = copy.copy(info)
#        fn = info2.filename = "debian/" + basefilename
#        if substitute and fn in substitute and substitute[fn] is None:
#          continue
#        if output_zip is not None:
#          if substitute and fn in substitute:
#            data = substitute[fn]
#          else:
#            data = input_zip.read(info.filename)
#          output_zip.writestr(info2, data)
#        if fn.endswith("/"):
#          Item.Get(fn[:-1], dir=True)
#        else:
#          Item.Get(fn, dir=False)
#
#  symlinks.sort()
#  return symlinks
#
#
#def InstallBoot(info):
#    # Install boot files
#    for filename in fnmatch.filter(info.input_zip.namelist(), "BOOT_PARTITION/*"):
#        fobj = info.input_zip.read(filename)
#        common.ZipWriteStr(info.output_zip, filename, fobj)
#    info.script.Mount("/boot")
#    info.script.UnpackPackageDir("BOOT_PARTITION", "/boot")
#
#def InstallDebian(info):
#    for filename in fnmatch.filter(info.input_zip.namelist(), "DEBIAN/*"):
#        fobj = info.input_zip.read(filename)
#        common.ZipWriteStr(info.output_zip, filename, fobj)
#    info.script.Mount("/debian")
#    info.script.UnpackPackageDir("DEBIAN", "/debian")
#
#    symlinks = CopyDebianFiles(info.input_zip)
#    info.script.MakeSymlinks(symlinks)
#
#    Item.GetMetadata(info.input_zip)
#    Item.Get("debian").SetPermissions(info.script)
#
#def LoadRecovery(info):
#    for filename in fnmatch.filter(info.input_zip.namelist(), "RECOVERY_PARTITION/*"):
#        fobj = info.input_zip.read(filename)
#        common.ZipWriteStr(info.output_zip, filename, fobj)
#    # Don't write anything out, we'll do that in coreshim
#
#
#
#def FullOTA_InstallEnd(info):
#    InstallBoot(info)
#    InstallDebian(info)
#    LoadRecovery(info)
#=======
# Copyright (C) 2016 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Emit extra commands needed for Group during OTA installation
(installing the bootloader)."""

import common
import fnmatch

#def InstallRecovery(info):
#  # Copy ramdisk (we use the same bootscript/kernel/dtbs as BOOT)
#  common.ZipWriteStr(info.output_zip, filename, file)
#  info.script.AppendExtra('package_extract_file("BOOTLOADER/SPL", "/SPL");')

def InstallBoot(info):
  # Copy bootscript/kernel/dtbs to output
  for filename in fnmatch.filter(info.input_zip.namelist(), "BOOT/boot/*"):
    file = info.input_zip.read(filename)
    common.ZipWriteStr(info.output_zip, filename, file)
  # Install
  #info.script.FormatPartition("/boot")
  info.script.Mount("/boot")
  info.script.UnpackPackageDir("BOOT", "/boot")

def InstallBootloader(info):
  # Copy SPL, u-boot.img to output
  for filename in fnmatch.filter(info.input_zip.namelist(), "BOOTLOADER/*"):
    file = info.input_zip.read(filename)
    common.ZipWriteStr(info.output_zip, filename, file)
  # Install SPL, u-boot.img, and erase u-boot environment
  info.script.AppendExtra('package_extract_file("BOOTLOADER/SPL", "/SPL");')
  info.script.AppendExtra('package_extract_file("BOOTLOADER/u-boot.img", "/u-boot.img");')
  info.script.AppendExtra('run_program("/sbin/kobs-ng", "init", "-v", "-x", "--search_exponent=1", "--chip_0_size=0xe00000", "--chip_0_device_path=/dev/mtd/mtd0", "/SPL");')
  info.script.AppendExtra('run_program("/sbin/flash_erase", "/dev/mtd/mtd0", "0xe00000", "0");')
  info.script.AppendExtra('run_program("/sbin/nandwrite", "--start=0xe00000", "--pad", "/dev/mtd/mtd0", "/u-boot.img");')
  # Erase bootloader env (if desired)
  #info.script.AppendExtra('run_program("/sbin/flash_erase", "/dev/mtd/mtd1", "0", "0");')

# called on the final stage of recovery:
#   wipe/install system(done for us), boot, and bootloader
def FullOTA_InstallEnd_Ext4(info):
  InstallBoot(info)
  InstallBootloader(info)
  #InstallRecovery(info)

def FullOTA_InstallEnd_Ubifs(info):
  InstallBoot(info)
  InstallBootloader(info)
  #InstallRecovery(info)

def IncrementalOTA_InstallBegin(info):
  info.script.Unmount("/system")
  info.script.TunePartition("/system", "-O", "^has_journal")
  info.script.Mount("/system")
