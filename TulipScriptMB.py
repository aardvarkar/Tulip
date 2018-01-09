# Powered by Python 2.7

# To cancel the modifications performed by the script
# on the current graph, click on the undo button.

# Some useful keyboards shortcuts : 
#   * Ctrl + D : comment selected lines.
#   * Ctrl + Shift + D  : uncomment selected lines.
#   * Ctrl + I : indent selected lines.
#   * Ctrl + Shift + I  : unindent selected lines.
#   * Ctrl + Return  : run script.
#   * Ctrl + F  : find selected text.
#   * Ctrl + R  : replace selected text.
#   * Ctrl + Space  : show auto-completion dialog.

from tulip import tlp
import random

# The updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# The pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# The runGraphScript(scriptFile, graph) function can be called to launch
# another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# The main(graph) function must be defined 
# to run the script on the current graph

def pretraitement(graph, Locus, Negative, Positive, viewBorderColor, viewLabel, viewLayout, viewSize):
  for n in graph.getNodes():
    print(n)
   
  size = 1000
  for n in graph.getNodes():
    x = random.random() * size
    y = random.random() * size
    viewLayout[n] = tlp.Coord(x, y, 0)
    viewSize[n] = tlp.Size(10,10,10)
    viewLabel[n] = Locus[n]
  for n in graph.getEdges():
    if Negative[n] == True:
      if Positive[n] == True:
        viewBorderColor[n] = tlp.Color.Blue
      else:
        viewBorderColor[n] = tlp.Color.Green
    elif Positive[n] == True:
      viewBorderColor[n] = tlp.Color.Red
    else:
      viewBorderColor[n] = tlp.Color.Violet
      
def applyModelForce(graph, viewLayout):
  params = tlp.getDefaultPluginParameters('FM^3 (OGDF)', graph)
  success = graph.applyLayoutAlgorithm('FM^3 (OGDF)', viewLayout, params)
  
 
def partitionnement1(working, tp17_s):
  for n in graph.getEdges():
    poids = abs(tp17_s[graph.source(n)]-tp17_s[graph.target(n)])
    print(poids)

def main(graph): 
  


  #
  clone = working.addCloneSubGraph("Clone")
  working = graph.addCloneSubGraph("Working")
  
  Locus = working.getStringProperty("Locus")
Negative = working.getBooleanProperty("Negative")
Positive = working.getBooleanProperty("Positive")
tp1_s = working.getDoubleProperty("tp1 s")
tp10_s = working.getDoubleProperty("tp10 s")
tp11_s = working.getDoubleProperty("tp11 s")
tp12_s = working.getDoubleProperty("tp12 s")
tp13_s = working.getDoubleProperty("tp13 s")
tp14_s = working.getDoubleProperty("tp14 s")
tp15_s = working.getDoubleProperty("tp15 s")
tp16_s = working.getDoubleProperty("tp16 s")
tp17_s = working.getDoubleProperty("tp17 s")
tp2_s = working.getDoubleProperty("tp2 s")
tp3_s = working.getDoubleProperty("tp3 s")
tp4_s = working.getDoubleProperty("tp4 s")
tp5_s = working.getDoubleProperty("tp5 s")
tp6_s = working.getDoubleProperty("tp6 s")
tp7_s = working.getDoubleProperty("tp7 s")
tp8_s = working.getDoubleProperty("tp8 s")
tp9_s = working.getDoubleProperty("tp9 s")
viewBorderColor = working.getColorProperty("viewBorderColor")
viewBorderWidth = working.getDoubleProperty("viewBorderWidth")
viewColor = working.getColorProperty("viewColor")
viewFont = working.getStringProperty("viewFont")
viewFontSize = working.getIntegerProperty("viewFontSize")
viewIcon = working.getStringProperty("viewIcon")
viewLabel = working.getStringProperty("viewLabel")
viewLabelBorderColor = working.getColorProperty("viewLabelBorderColor")
viewLabelBorderWidth = working.getDoubleProperty("viewLabelBorderWidth")
viewLabelColor = working.getColorProperty("viewLabelColor")
viewLabelPosition = working.getIntegerProperty("viewLabelPosition")
viewLayout = working.getLayoutProperty("viewLayout")
viewMetric = working.getDoubleProperty("viewMetric")
viewRotation = working.getDoubleProperty("viewRotation")
viewSelection = working.getBooleanProperty("viewSelection")
viewShape = working.getIntegerProperty("viewShape")
viewSize = working.getSizeProperty("viewSize")
viewSrcAnchorShape = working.getIntegerProperty("viewSrcAnchorShape")
viewSrcAnchorSize = working.getSizeProperty("viewSrcAnchorSize")
viewTexture = working.getStringProperty("viewTexture")
viewTgtAnchorShape = working.getIntegerProperty("viewTgtAnchorShape")
viewTgtAnchorSize = working.getSizeProperty("viewTgtAnchorSize")

  print(Locus)
  pretraitement(working, Locus, Negative, Positive, viewColor, viewLabel, viewLayout, viewSize)
  applyModelForce(working, viewLayout)
  #partitionnement1(working, tp17_s)
