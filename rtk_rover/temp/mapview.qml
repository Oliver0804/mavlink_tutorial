import QtQuick 2.0
import QtLocation 5.6

Map {
    plugin: Plugin {
        name: "osm" // OpenStreetMap plugin, you might need to use a custom plugin for offline maps
        // Set up parameters for offline mode
        PluginParameter { name: "osm.mapping.offline.directory"; value: "path_to_offline_tiles" }
        PluginParameter { name: "osm.mapping.offline.coverage"; value: "coverage area definition" }
    }
    center: QtPositioning.coordinate(25.0330, 121.5654) // Taipei 101 coordinates
    zoomLevel: 15
}
