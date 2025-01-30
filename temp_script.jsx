
    var filePath = 'E:\Archives\Gigamon Project\a project\Made by AI\Bing\male\_0a8de76c-8474-4123-81e6-69741159038b.jpg';
    var selectionBounds = [50, 50, 200, 200];

    function contentAwareFill(bounds) {
        var doc = app.activeDocument;
        doc.selection.select([[bounds[0], bounds[1]], [bounds[2], bounds[1]], [bounds[2], bounds[3]], [bounds[0], bounds[3]]]);
        doc.selection.fill(app.fillContents);
    }

    contentAwareFill(selectionBounds);
    