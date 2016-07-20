L.mapbox.accessToken = 'pk.eyJ1IjoiaGl2YW1zZWUiLCJhIjoiY2lraGFyMHRiMDFjeXYwa21mdWYxb2t0NiJ9.DaVAaeEszhOTuPzxZyCFwA';
var map = L.mapbox.map('map', 'mapbox.streets')
    .setView([42.288138, -83.69706], 13);
omnivore.csv('/home/vamsee/new/CarWise/2304.csv').addTo(map);