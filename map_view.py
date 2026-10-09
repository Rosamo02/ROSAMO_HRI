from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PySide6.QtCore import QUrl
import os
#Configures the QWebEngineView widget to display the HTML-based map.
#Enables JavaScript, allows access to local and remote resources, configures geolocation permissions, and loads the map HTML file.
def setup_map(view):
    settings = view.settings()
    settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
    settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
    settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)

    profile = view.page().profile()
    profile.setPersistentStoragePath(os.path.expanduser("~/.qtwebengine"))
    profile.settings().setAttribute(QWebEngineSettings.AllowGeolocationOnInsecureOrigins, True)

    page = view.page()
    page.consoleMessage = lambda level, msg, line, source: print("JS:", msg)

    def handle_permission(url, feature):
        print("Permission requested:", feature)
        if feature == QWebEnginePage.Geolocation:
            page.setFeaturePermission(
                url,
                QWebEnginePage.Geolocation,
                QWebEnginePage.PermissionGrantedByUser
            )

    page.featurePermissionRequested.connect(handle_permission)
    # Get the directory where this Python script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Build the path to the HTML file inside the map_assets folder
    html_path = os.path.join(script_dir, "map_assets", "map.html")
    
    # Load the local HTML map into the QWebEngineView widget
    view.load(QUrl.fromLocalFile(html_path))
