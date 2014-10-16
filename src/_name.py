import site
site.addsitedir(r"R:\Pipe_Repo\Users\Qurban\utilities")
import qtify_maya_window as qtfy
from uiContainer import uic
import pymel.core as pc
import os.path as osp
import appUsageApp
reload(appUsageApp)

root_path = osp.dirname(osp.dirname(__file__))
ui_path = osp.join(root_path, 'ui')

Form, Base = uic.loadUiType(osp.join(ui_path, 'main.ui'))
class Name(Form, Base):
    def __init__(self, parent=qtfy.getMayaWindow()):
        super(Name, self).__init__(parent)
        self.setupUi(self)
        
        self.mappings = {'aiMatteColor': 'matteColor',
                         'aiMatteColorA': 'matteOpacity',
                         'color': 'diffuseColor',
                         'Kd': 'diffuseWeight',
                         'Kb': 'diffuseBackLighting',
                         'KsColor': 'specularColor',
                         'Ks': 'specularWeight',
                         'Ksn': 'specularReflectanceAtNormal',
                         'KrColor': 'reflectionColor',
                         'Kr': 'reflectionWeight',
                         'Krn': 'reflectionReflectanceAtNormal',
                         'KtColor': 'refractionColor',
                         'Kt': 'refractionWeight',
                         'normalCamera': 'bumpMapping',
                         'KsssColor': 'subSurfaceScatteringColor',
                         'Ksss': 'subSurfaceScatteringWeight',
                         'sssRadius': 'subSurfaceScatteringRadius',
                         'emision': 'emissionScale'}
        
        self.okButton.clicked.connect(self.name)
        self.nameBox.returnPressed.connect(self.name)
        
        appUsageApp.updateDatabase('nameMtl')
        
    def closeEvent(self, event):
        self.deleteLater()
        
    def name(self):
        name = str(self.nameBox.text())
        if not name:
            pc.warning('Name not specified...')
            return
        try:
            mtl = pc.ls(sl=True)[0]
        except IndexError:
            pc.warning('No selection found')
            return
        if pc.objExists(name):
            pc.warning('An object named "%s" of type "%s" already exists in the scene'%(name, pc.PyNode(name).nodeType()))
            return
        try:
            pc.rename(mtl, name+'_mtl')
        except Exception as ex:
            pc.warning(str(ex)+' ('+node.name()+')')
            return
        for node in pc.listConnections(mtl):
            if type(node) == pc.nt.ShadingEngine:
                pc.rename(node, name+'SG')
                continue
            dest = node.outputs(plugs=True) + node.inputs(plugs=True)
            for ds in dest:
                if ds.node().name() == mtl.name():
                    ds = ds.name().split('.')[-1]
                    niceName = self.mappings.get(ds)
                    ds = niceName if niceName else ds
                    try:
                        pc.rename(node, name+'_'+ds)
                    except Exception as ex:
                        pc.warning(str(ex)+' ('+node.name()+')')
                    break