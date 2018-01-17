#Author-Conor O'Rourke
#Description-Simple check of constraint status

import adsk.core, adsk.fusion, adsk.cam, traceback


#
# Globals
#

g_ui = None
g_design = None




#
# Fusion 360 call entry point, run()
#

def run(context):
    global g_ui, g_design
    g_ui = None
    g_design = None

    try:
        app = adsk.core.Application.get()
        g_ui  = app.userInterface

        g_design = app.activeProduct
        if not isinstance(g_design, adsk.fusion.Design):
            g_ui.messageBox("Not supported. Please use MODEL workspace.")
            return

        activeSketch = app.activeEditObject

        if activeSketch.objectType != adsk.fusion.Sketch.classType():
            g_ui.messageBox("You aren't inside an active sketch!")
            return

        if activeSketch.isFullyConstrained:
            g_ui.messageBox("This sketch seems to be fully constrained")
        else:
            g_ui.messageBox("This sketch is not fully constrained")

    except:
        if g_ui:
            g_ui.messageBox("Failed:\n{}".format(traceback.format_exc()))

