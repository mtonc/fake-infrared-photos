# Fake Infrared Photos

This script will load images from a file, folder, or url. It will then isolate the selected band (R for infrared) and convert to gray scale before saving the new image.

# Usage
### File mode
```
python3 infrared.py --file[-f] images/some_image_file.jpg --band R
```
### Folder mode
```
python3 infrared.py --directory[-d] images/ --band G
```

### URL mode
```
python3 infrared.py --url[-u] --band B
```
