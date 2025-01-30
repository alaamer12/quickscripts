import subprocess
import os
def generate_photoshop_script(selection_bounds, script_path):
    script_content = f"""
#target photoshop

function contentAwareFill(selectionBounds) {{
    if (app.documents.length > 0) {{
        var doc = app.activeDocument;

        // Create a selection based on the provided bounds
        doc.selection.select(selectionBounds);

        // Perform content-aware fill
        doc.selection.fill(app.foregroundColor, ContentAware, 100, false);

        // Deselect the selection
        doc.selection.deselect();
    }}
}}

// Example selection bounds (left, top, right, bottom)
var selectionBounds = {selection_bounds};
contentAwareFill(selectionBounds);
"""

    with open(script_path, 'w') as script_file:
        script_file.write(script_content)

def run_photoshop_script(script_path):
    photoshop_executable = r"F:\Program Files\Adobe\Photoshop\Adobe Photoshop CC 2019\Photoshop.exe"
    subprocess.run([photoshop_executable, "-r", script_path])

# Example usage
selection_bounds = [[50, 50], [200, 50], [200, 200], [50, 200]]

script_path = f"{os.getcwd()}/content_aware_script.jsx"
generate_photoshop_script(selection_bounds, script_path)
run_photoshop_script(script_path)
