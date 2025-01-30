
#target photoshop

function contentAwareFill(selectionBounds) {
    if (app.documents.length > 0) {
        var doc = app.activeDocument;

        // Create a selection based on the provided bounds
        doc.selection.select(selectionBounds);

        // Perform content-aware fill
        doc.selection.fill(app.foregroundColor, ContentAware, 100, false);

        // Deselect the selection
        doc.selection.deselect();
    }
}

// Example selection bounds (left, top, right, bottom)
var selectionBounds = [[50, 50], [200, 50], [200, 200], [50, 200]];
contentAwareFill(selectionBounds);
