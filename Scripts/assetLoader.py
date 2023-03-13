import os, tomllib, pygame as pyg
from main import NextID
programPath = os.getcwd()


def loadImageAsset(fileName):
    return pyg.image.load(programPath+fileName).convert()

def loadAssetData():
    with open(os.getcwd()+r'\ConfigFiles\assetData.toml', "rb") as f:
        dataFile = tomllib.load(f)
        print(dataFile)
    loadedAssets = {}
    for data in dataFile["assets"]["place"].values():
        loadedAssets[NextID(loadedAssets)] = loadImageAsset(data)
    return loadedAssets