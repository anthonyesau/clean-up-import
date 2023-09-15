## Installation

1. Download the add-on from the Github repository in .zip format. To do this, click on the green "Code" button and then select "Download ZIP".
2. Open Blender and navigate to Edit > Preferences > Add-ons.
3. Click on the "Install" button located at the top right corner of the window.
4. Navigate to the directory where you downloaded the ZIP file and select it.
5. Click "Install Add-on" and wait for the add-on to install.
6. Once installed, make sure the add-on is enabled by checking the checkbox next to the add-on name in the Add-ons list.
7. Save your preferences to ensure that the add-on is available when you open Blender in the future. Blender auto-saves preferences by default.

That's it! You should now be able to use the add-on in Blender.

## Material Swapper

Select one material to swap for another. Helpful for comparing two different paint colors. 

**[ ] Swap on Selected Only:** When enabled, only materials on only the selected objects will be affected. When disabled, all materials within the scene will be affected.

**[ ] Protect Removed Material (Add Fake User):** Prevents the material that was removed from being purged by adding a fake user. Otherwise, the removed material may be deleted from the file the next time it is opened when unlinked data is purged—if the material has no other users in the entire file. You may want to keep the removed material around to reference and compare in the future.

**Swap Material Link:**
- **Link to Object:** Useful for applying different materials to separate instances of shared mesh data.
- **Link to Data:** All instances of the mesh data will have the same material. This is Blender's default setting. 
- **No Change:** Leave this setting unchanged.

## Relink Images with Suffix Resolver

Select files on disk to re-link to existing image assets. The suffix resolver will link image assets with suffixes such as "Bottle 2 from St. Juliana Color.png" and "Bottle 2 from St. Juliana Transparency.png" to the selected file "Bottle 2 from St. Juliana.png." The suffix must be separated from the primary part of the filename with a space character. 

**Absolute or relative paths:** Note that in the file picker, you can choose to relink with absolute or relative paths. Relative paths work well when the Blender file is synced to a cloud service like Dropbox and multiple people access it. 

**Dev notes:** The ability to match the first word (the characters *before* the first space character) is in the code but disabled because it resulted in too many false matches. It may be worth reviewing if it can be implemented in a functional way, perhaps as an option the user can select. Or perhaps this functionality should be split out into a separate tool or removed.

## CleanVWImageNames

## CorrectGamma

## CustomPanel

## DeleteVWCamera

## DeleteVWLights

## Merge Duplicate Images

Remaps `material_name.002` and `material_name.003` to `material_name`. 

If no `material_name` already exists, `material_name.002` will be renamed to `material_name`.

Remaps multiple image data with the same filepath to the first image data that includes that filepath. The list of images is in ascending order based on name ('a' before 'b', '1' before '2', et cetera). 

## MergeDuplicateMaterials

Remaps `material_name.002` and `material_name.003` to `material_name`. 

If no `material_name` already exists, `material_name.002` will be renamed to `material_name`.

## FormatVWAreaLights

## DissolveTopVWEmpties

## EnableAutoSmooth

## ResequenceObjectNames
