from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PySide6.QtCore import QUrl
import os

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

    html_path = "/home/rodrigomoreira/Rosamo_3/map_assets/map.html"
    view.load(QUrl.fromLocalFile(html_path))
