function log(node_name, msg) {
    //if ((node_name!='#camera_log') || (node_name='#camera_log' && gTrackCamera)) {
        $(node_name).append("<span>" + msg + "</span><br />")
    //}
}

function log_reset() {
    $("#camera_log").html("");
}

function reset_aff_results() {
    $('#aff_res1').html("");
    $('#aff_res2').html("");
}

function log_affdex_reset() {
    document.getElementById("log_affdex").value = "";
}

function log_xlabs_reset() {
    //document.getElementById("log_xlabs").value = "";
}

function log_events_reset() {
    document.getElementById("log_events").value = "";
}

function log_events_write(event) {
    if (gTrackButtons) {
        var timeStamp = (new Date()).getTime();
        document.getElementById("log_events").value += '{"timestamp":' + timeStamp + ',"event":"' + event + '"}' + "\n";
    }
}





function btn_camera_start() {
    if (detector && !detector.isRunning) {
        log_reset();
        log_affdex_reset();
        log_xlabs_reset();
    }
    log('#camera_log', "Clicked the start button");
    if (detector && !detector.isRunning) {
        detector.start();
        xlabs_start();
    }
}

function btn_camera_stop() {
    log('#camera_log', "Clicked the stop button");
    if (detector && detector.isRunning) {
        detector.removeEventListener();
        detector.stop();
        xlabs_stop();
        if (gTrackXlabs) {
            xlabs_refresh();
        }
    }
}

function btn_camera_reset() {
    log('#camera_log', "Clicked the reset button");
    if (detector && detector.isRunning) {
        detector.reset();
        reset_aff_results();
        xlabs_refresh();
    }
};

function btn_survey_start() {
    log_events_write('survey_start');
    showSurvey();
    document.getElementById('divStartQuiz').style.display = 'none';
}
