# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Infoworks2raster
                                 A QGIS plugin
 Rasteriza resultados de Infoworks ICM
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-11-18
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Jhon E. Chahua Janampa
        email                : chahua.evar@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import (QSettings,
                              QTranslator, QCoreApplication)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (QAction, QFileDialog,
                                 QMessageBox, QToolTip)
from qgis.core import *
from qgis.core import QgsProject, QgsRasterLayer

#
from qgis.processing import run
#

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .Infoworks2raster_dialog import Infoworks2rasterDialog
import os.path
import tempfile


class Infoworks2raster:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Infoworks2raster_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Resultados - Infoworks ICM')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Infoworks2raster', message)
    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        #2-añadido
        self.dlg= Infoworks2rasterDialog()
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Infoworks2raster/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Rasterizador'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True
#añadido       
        self.dir = tempfile.gettempdir()
        self.dlg.btnRasterizar.clicked.connect(self.btnRasterizar_click)
        self.dlg.btnRuta.clicked.connect(self.btnRuta_click)
        self.dlg.btnActualizar.clicked.connect(self.btnActualizar_click)
        self.dlg.btnActualizar.setToolTip("Actualizar capas")
#fin añadido
        

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Resultados - Infoworks ICM'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

#inicio añadido
        self.dlg.cmbLayers.clear()
        layers=[]

        """for tree_layer in QgsProject.instance().layerTreeRoot().findLayers():
            layers.append(tree_layer.layer())"""

        for tree_layer in QgsProject.instance().layerTreeRoot().findLayers():
            laier = tree_layer.layer()

            if laier.type() == QgsMapLayerType.VectorLayer and laier.geometryType() == QgsWkbTypes.PolygonGeometry:
                layers.append(tree_layer.layer())    

        layer_list=[]

        for layer in layers:
            layer_list.append(layer.name())

        layer_list.insert(0,'Seleccione una capa')

        self.dlg.cmbLayers.addItems(layer_list)

        #capa_seleccionada= self.dlg.cmbLayers.addItems(layer_list)

        self.dlg.Resolucion.clear()
        self.dlg.Nombre.clear()
        self.dlg.leRuta.clear()

        self.dlg.leRuta.setText(tempfile.gettempdir())
        self.dlg.Resolucion.setText("0.")
        self.dlg.Nombre.setText("TR")

        
# fin añadido

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass


    def btnActualizar_click(self):
        self.dlg.cmbLayers.clear()
        layers=[]
        for tree_layer in QgsProject.instance().layerTreeRoot().findLayers():
            laier = tree_layer.layer()
            if laier.type() == QgsMapLayerType.VectorLayer and laier.geometryType() == QgsWkbTypes.PolygonGeometry:
                layers.append(tree_layer.layer())    
        layer_list=[]
        for layer in layers:
            layer_list.append(layer.name())
        self.dlg.cmbLayers.addItems(layer_list)
    
    def btnRuta_click(self):
        carpeta_seleccionada = QFileDialog.getExistingDirectory(None,
            "Seleccionar Carpeta", "")

        if carpeta_seleccionada:
            # Almacenar la ruta seleccionada en la variable de instancia
            self.carpeta_seleccionada = carpeta_seleccionada
            # Mostrar la ruta en el QTextEdit
            self.dlg.leRuta.setText(carpeta_seleccionada)
        #self.iface.mainWindow()

        if not carpeta_seleccionada:
            return
        #self.iface.mainWindow()

        

    def btnRasterizar_click(self):
        layer_name = self.dlg.cmbLayers.currentText()

        #Verificar si se seleccionó una carpeta
        if not layer_name or layer_name == "Seleccione una capa":
            QMessageBox.warning(None, "Rasterizador - Infoworks ICM",
                "Debe seleccionar una capa válida")
            return
        
        resolucion = float(self.dlg.Resolucion.toPlainText())

        if not resolucion or resolucion <= 0:
            QMessageBox.warning(None, "Rasterizador - Infoworks ICM",
                "Debe colocar un valor de resolución válido")
            return

        ruta_salida = self.dlg.leRuta.text()
        nombre_raster1 = str("MFD-" + self.dlg.Nombre.toPlainText())
        nombre_raster2 = str("MFV-" + self.dlg.Nombre.toPlainText())
       
        # Obtener la capa seleccionada
        capa = QgsProject.instance().mapLayersByName(layer_name)[0]

        # Configurar opciones de procesamiento
        parameters_MFD = {
            'INPUT': capa,
            'FIELD':'DEPTH2D',
            'BURN':0,
            'USE_Z':False,
            'UNITS':1,
            'WIDTH':resolucion,
            'HEIGHT':resolucion,
            'EXTENT':QgsProject.instance().crs(),
            'NODATA':0,
            'OPTIONS':'',
            'DATA_TYPE':5,
            'INIT':None,
            'INVERT':False,
            'EXTRA':'',
            'OUTPUT':f"{ruta_salida}/{nombre_raster1}.tif"
        }
        parameters_MFV = {
            'INPUT': capa,
            'FIELD':'SPEED2D',
            'BURN':0,
            'USE_Z':False,
            'UNITS':1,
            'WIDTH':resolucion,
            'HEIGHT':resolucion,
            'EXTENT':QgsProject.instance().crs(),
            'NODATA':0,
            'OPTIONS':'',
            'DATA_TYPE':5,
            'INIT':None,
            'INVERT':False,
            'EXTRA':'',
            'OUTPUT':f"{ruta_salida}/{nombre_raster2}.tif"
        }

        # Ejecutar el algoritmo de rasterización
        resultado1= run("gdal:rasterize", parameters_MFD)
        resultado2= run("gdal:rasterize", parameters_MFV)

        if resultado1['OUTPUT']:
            capa_raster1 = QgsRasterLayer(resultado1['OUTPUT'], nombre_raster1)
            QgsProject.instance().addMapLayer(capa_raster1)
        if resultado2['OUTPUT']:
            capa_raster2 = QgsRasterLayer(resultado2['OUTPUT'], nombre_raster2)
            QgsProject.instance().addMapLayer(capa_raster2)
        QMessageBox.information(None, "Rasterizador - Infoworks ICM",
                "Proceso finalizado - capas cargadas")