bl_info = {
    "name": "AE Utilz",
    "author": "Anthony Esau",
    "version": (0, 24),
    "blender": (3, 5, 0),
    "location": "",
    "description": "",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": ""
}

modulesNames = [\
    "CleanVWImageNames", \
    "CorrectGamma", \
    "CustomPanel", \
    "DeleteVWCamera", \
    "DeleteVWLights", \
    "MergeDuplicateImages", \
    "MergeDuplicateMaterials", \
    "ConnectAlpha", \
    "SetImgNodeSRGB", \
    "SetAlphaBlendMode", \
    "FormatVWAreaLights", \
    "DissolveTopVWEmpties", \
    "EnableAutoSmooth", \
    "ResequenceObjectNames", \
    "MaterialSwapper", \
    "RelinkImages",\
    "Batch rename images"\
]
 
import sys
import importlib
 
modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))
 
for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)
 
def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()
 
def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
 
if __name__ == "__main__":
    register()