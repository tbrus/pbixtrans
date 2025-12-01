from pbixtrans.layout.visuals.actionbutton import translate_actionbutton
from pbixtrans.layout.visuals.slicer import translate_slicer
from pbixtrans.layout.visuals.textbox import translate_textbox

VISUAL_TRANSLATORS = {
    "actionButton": translate_actionbutton,
    "slicer": translate_slicer,
    "textbox": translate_textbox,
}