var xLabsVar = {
    cameraStart : function() {
        xLabs.setConfig( "frame.stream.enabled", "1" );
        xLabs.setConfig( "system.mode", "learning" );
    },
    cameraStop : function() {
        xLabs.setConfig( "frame.stream.enabled", "0" );
        xLabs.setConfig( "system.mode", "off" );
    },
    ready : function() {
        xLabs.setConfig( "gaze.temp.enabled", "1" );
        xLabs.setConfig( "system.mode", "off" );
        xLabs.setConfig( "browser.canvas.paintLearning", "0" );
    },
    idPath : function( id, path ) {
        console.log( "id="+id+" path="+path );
    },            
    update : function() {
        //onXlabsUpdate();
    },
    refresh : function() {
        xLabs.setConfig( "gaze.temp.id", "log_xlabs" );
    }
};

function xlabs_start() {
    xLabsVar.cameraStart();
    log('#camera_log', "xLabs: Start");
}

function xlabs_stop() {
    xLabsVar.cameraStop();
    log('#camera_log', "xLabs: Stop");
}

function xlabs_refresh() {
    xLabsVar.refresh();
    log('#camera_log', "xLabs: Refresh");
}

/*
function submit_handler() {
    alert("Submission validation");
    gaze_logs = document.getElementById("log_xlabs");
    if (gaze_logs=="Here will come gaze logs...")
        return false;
    else{
        alert("Submit the form");
        return true;
    }
}*/
 
function onXlabsUpdate() {
    //log('#track_log', '{test}');
    /*
    var xs = parseFloat( xLabs.getConfig( "state.gaze.estimate.x" ) );
    var ys = parseFloat( xLabs.getConfig( "state.gaze.estimate.y" ) );        
    if( !xLabs.documentOffsetReady() ) {
        return;
    }
    
    var trackingSuspended = parseInt( xLabs.getConfig( "state.trackingSuspended" ) );
    var calibrationStatus = parseInt( xLabs.getConfig( "calibration.status" ) );
    if( ( calibrationStatus == 0 ) || ( trackingSuspended == 1 ) ) {
        return;
    }            
    var x = xLabs.scr2docX( xs );
    var y = xLabs.scr2docY( ys );
    var c = parseFloat( xLabs.getConfig( "state.calibration.confidence" ) );
    //*/
}

xLabs.setup(xLabsVar.ready, xLabsVar.update, xLabsVar.idPath, "a59f7e14-518a-4c2f-8ee9-3180cbcfb817");

//document.getElementById("gaze_values").submit = submit_handler;

window.addEventListener( "beforeunload", function(event) {
    xLabsVar.cameraStop();
});