var locations = [
    {title: 'Park Ave Penthouse', location: {lat: 40.7713024, lng: -73.9632393}, visible: ko.observable(true), id: 0},
    {title: 'Chelsea Loft', location: {lat: 40.7444883, lng: -73.9949465}, visible: ko.observable(true), id: 1},
    {title: 'Union Square Open Floor Plan', location: {lat: 40.7347062, lng: -73.9895759}, visible: ko.observable(true), id: 2},
    {title: 'East Village Hip Studio', location: {lat: 40.7281777, lng: -73.984377}, visible: ko.observable(true), id: 3},
    {title: 'TriBeCa Artsy Bachelor Pad', location: {lat: 40.7195264, lng: -74.0089934}, visible: ko.observable(true), id: 4},
    {title: 'Chinatown Homey Space', location: {lat: 40.7180628, lng: -73.9961237}, visible: ko.observable(true), id: 5}
];

function ViewModel() {
    var self = this;
    // styling markers
    function makeMarkerIcon(markerColor) {
        return new google.maps.MarkerImage(
            'http://chart.googleapis.com/chart?chst=d_map_spin&chld=1.15|0|'+ markerColor +
            '|40|_|%E2%80%A2',
            new google.maps.Size(21, 34),
            new google.maps.Point(0, 0),
            new google.maps.Point(10, 34),
            new google.maps.Size(21,34));
    }
    let defaultIcon = makeMarkerIcon('0091ff');
    let highlightedIcon = makeMarkerIcon('FFFF24');

    // create map
    var markers = [];
    var bounds = new google.maps.LatLngBounds();
    this.shownLocations = ko.observableArray(locations);
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 40.7413549, lng: -73.9980244},
        zoom: 13,
        mapTypeControl: false
    });
    let largeInfowindow = new google.maps.InfoWindow();
    for (let i = 0; i < locations.length; i++) {
        let position = locations[i].location;
        let title = locations[i].title;
        let marker = new google.maps.Marker({
            map: map,
            position: position,
            title: title,
            animation: google.maps.Animation.DROP,
            icon: defaultIcon,
            id: i
        });
        markers.push(marker);
        marker.addListener('click', function() {
            populateInfoWindow(this, largeInfowindow);
        }); 
        marker.addListener('mouseover', function() {
            this.setIcon(highlightedIcon);
        });
        marker.addListener('mouseout', function() {
            this.setIcon(defaultIcon);
        });
        // $("#list-view").append("<li id='location-" + i + "'>" + title + "</li>")
        bounds.extend(marker.position);
        console.log(this.shownLocations()[i].title);
    }
    // for (let i = 0; i < locations.length; i++) {
    //     console.log("#location-" + i);
    //     $("#location-" + i).addListener('click', function() {
    //         chosenLocation(this, largeInfowindow);
    //     });
    // }
    map.fitBounds(bounds);

    this.locationOnClick = function(location) {
        google.maps.event.trigger(markers[location.id], 'click');
    };

    this.filterInput = ko.observable('');
    this.filterOnClick = function() {
        // let locations = self.shownLocations();
        // let filterInput = self.filterInput();
        // locations.forEach(function(location) {
        //     if (location.title.toLowerCase().indexOf(filterInput.toLowerCase()) == -1) {
        //         location.visible(false);
        //         markers[location.id].setMap(null);
        //     } else {
        //         location.visible(true);
        //         markers[location.id].setMap(map);
        //     }
        // });
        let filterInput = self.filterInput();
        console.log(filterInput);
        for (let i = 0; i < self.shownLocations().length; i++) {
            let location = self.shownLocations()[i];
            if (location.title.toLowerCase().indexOf(filterInput.toLowerCase()) == -1) {
                self.shownLocations()[i].visible(false);
                markers[location.id].setMap(null);
            } else {
                self.shownLocations()[i].visible(true);
                markers[location.id].setMap(map);
            }
            //console.log(self.shownLocations()[i]().visible);
        }
    };
    
};

function populateInfoWindow(marker, infowindow) {
    // Check to make sure the infowindow is not already opened on this marker.
    if (infowindow.marker != marker) {
        infowindow.marker = marker;
        infowindow.setContent('<div>' + marker.title + '</div>');
        infowindow.open(map, marker);
        // Make sure the marker property is cleared if the infowindow is closed.
        infowindow.addListener('closeclick', function() {
          infowindow.marker = null;
        });
    }
}

function initMap() {
    ko.applyBindings(new ViewModel());
}