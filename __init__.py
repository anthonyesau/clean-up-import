bl_info = {
    "name": "AE Utilz",
    "author": "Anthony Esau",
    "version": (0, 29),
    "blender": (4, 4, 3),
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
    "ExtractVWDesignLayers", \
    "RecombineMeshes", \
    "EnableAutoSmooth", \
    "ResequenceObjectNames", \
    "MaterialSwapper", \
    "RelinkImages",\
    "RefreshImages",\
    "Batch rename images",\
    "SetOutputPath"
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