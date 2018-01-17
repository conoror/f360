#Author-Conor O'Rourke
#Description-Dump out user and model parameters to a file

import adsk.core, adsk.fusion, adsk.cam, traceback
import sys, os.path


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

        if sys.platform == "win32":
            import ctypes.wintypes

            CSIDL_PERSONAL = 5      # My Documents
            SHGFP_TYPE_CURRENT = 0  # Current value

            ucbuf = ctypes.create_unicode_buffer(
                    ctypes.wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(
                    0, CSIDL_PERSONAL, 0, SHGFP_TYPE_CURRENT, ucbuf)
            initialDirectory = ucbuf.value
        else:
            initialDirectory = os.path.expanduser("~")


        fileDialog = g_ui.createFileDialog()
        fileDialog.isMultiSelectEnabled = False
        fileDialog.initialDirectory = initialDirectory
        fileDialog.title = "Specify filename to write"
        fileDialog.filter = 'Text files (*.txt)'
        fileDialog.filterIndex = 0
        dialogResult = fileDialog.showSave()

        if dialogResult != adsk.core.DialogResults.DialogOK:
            return

        filename = fileDialog.filename

        outputFile = open(filename, 'w', encoding="utf-8")

        dump_user_params(outputFile)


        # For model parameters run through the Components, sort them by
        # name (except that root component should be first) and then call
        # dump_component_params() on each component.

        ComponentList = []
        collComps = g_design.allComponents

        for i in range(collComps.count):
            component = collComps.item(i)
            if component.name != g_design.rootComponent.name:
                ComponentList.append(component)

        SortedCompList = sorted(ComponentList, key=lambda cname: cname.name)
        SortedCompList.insert(0, g_design.rootComponent)

        for component in SortedCompList:
            dump_component_params(outputFile, component)

        outputFile.close()
        return

    except:
        if g_ui:
            g_ui.messageBox("Failed:\n{}".format(traceback.format_exc()))




def dump_user_params(output):

    output.write("User Parameters, Unit, Expression, Value, Comment\n")

    paramList = g_design.userParameters

    UserParams = []

    for i in range(paramList.count):
        param = paramList.item(i)
        UserParams.append(param)

    # Sort by name and output in field widths

    SortedParams = sorted(UserParams, key=lambda pname: pname.name)

    for param in SortedParams:
        pvalue = "{:.6f}".format(param.value).rstrip('0') + "0"

        output.write('{}, {}, "{}", {}, "{}"\n'.
                format(param.name, param.unit,
                       param.expression.replace('"', r'""'),
                       pvalue,
                       param.comment.replace('"', r'""')))

    output.write("\n")




def dump_component_params(output, component):

    if component.modelParameters is None:
        return

    paramList = component.modelParameters
    if paramList.count == 0:
        return

    output.write("{}, Unit, Expression, Value, Comment\n".
            format(component.name))

    ComponentParams = []

    for i in range(paramList.count):
        param = paramList.item(i)
        ComponentParams.append(param)

    # Sort by name and output in field widths

    SortedParams = sorted(ComponentParams, key=lambda pname: pname.name)

    for param in SortedParams:
        pvalue = "{:.6f}".format(param.value).rstrip('0') + "0"

        output.write('{}, {}, "{}", {}, "{}"\n'.
                format(param.name, param.unit,
                       param.expression.replace('"', r'""'),
                       pvalue,
                       param.role.replace('"', r'""')))

    output.write("\n")

