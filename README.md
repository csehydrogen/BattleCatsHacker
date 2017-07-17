# BattleCatsHacker

A tool for manipulating data of [BattleCats](https://play.google.com/store/apps/details?id=jp.co.ponos.battlecatsen&hl=en) (kr : 냥코대전쟁). Idea is based on [beeven's work](https://github.com/beeven/battlecats). Big thanks!

## Warning!

This tool targets ***korean*** version. For other version, the followings should be modified before you proceed :

* package name (kr : jp.co.ponos.battlecatskr)
* hash salt in SaveDataModifier.py (kr : battlecatskr, en : battlecats)

## Requirements

* Android Debug Bridge (adb)
* Android Backup Extractor (abe.jar)

I just dumped binaries into this repo.

## How-to

```
# let's work inside workspace directory
cd workspace
# dump battlecats' data as backup.ab
../adb backup jp.co.ponos.battlecatskr
# backup this to somewhere safe
cp backup.ab ../archive/`date '+%Y%m%d%H%M%S'`.ab
# convert ab to tar, extract it, and make list of files inside it
java -jar ../abe.jar unpack backup.ab backup.tar
tar -xf backup.tar
tar -tf backup.tar > backup.list

# ...
# get apps/jp.co.ponos.battlecatskr/sp/save.xml
# modify it using probe.py and modify.py
# ...

# reverse process
star -c -f backup.tar -no-dirslash list=backup.list
java -jar ../abe.jar pack backup.tar backup.ab
../adb restore backup.ab
```

## savedata byte layout

```
catfood
7
exp
75
unit storage
y + 4x = unitid
y + 4x = type (1 = normal, 2 = castle)
eyes
y + 4x = # of eyes (4 types)
fruit storage
y + 4x = # of fruits (11 types) (purple, red, blue, green, yellow)
items
y + 4x = # of items (6 types)
```