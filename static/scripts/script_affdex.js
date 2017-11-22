// SDK Needs to create video and canvas nodes in the DOM in order to function
// Here we are adding those nodes a predefined div.
var divRoot = $("#affdex_elements")[0];
var width = 200;//640;
var height = 150;//480;
var faceMode = affdex.FaceDetectorMode.LARGE_FACES;
var showPoints = false;

//Construct a CameraDetector and specify the image width / height and face detector mode.
var detector = new affdex.CameraDetector(divRoot, width, height, faceMode);

//Enable detection of all Expressions, Emotions and Emojis classifiers.
detector.detectAllEmotions();
detector.detectAllExpressions();
detector.detectAllEmojis();
detector.detectAllAppearance();

//Add a callback to notify when the detector is initialized and ready for running.
detector.addEventListener("onInitializeSuccess", function() {
    log('#camera_log', "AFF: The detector reports initialized");
    btn_survey_enable();
    
    //Display canvas instead of video feed because we want to draw the feature points on it
    if (showPoints) {
        $("#face_video_canvas").css("display", "block");
        $("#face_video").css("display", "none");
    }
});

//Add a callback to notify when camera access is allowed
detector.addEventListener("onWebcamConnectSuccess", function() {
    log('#camera_log', "AFF: Webcam access allowed");
});

//Add a callback to notify when camera access is denied
detector.addEventListener("onWebcamConnectFailure", function() {
    log('#camera_log', "AFF: Webcam access denied");
    console.log("Webcam access denied");
});

//Add a callback to notify when detector is stopped
detector.addEventListener("onStopSuccess", function() {
    log('#camera_log', "AFF: The detector reports stopped");
    //reset_aff_results();
});

//Add a callback to receive the results from processing an image.
//The faces object contains the list of the faces detected in an image.
//Faces object contains probabilities for all the different expressions, emotions and appearance metrics
detector.addEventListener("onImageResultsSuccess", function(faces, image, timestamp) {
    if (gTrackAff) {
        if (faces.length > 0) {
            jnom = '{"app":"affdex"}';
            //jtim = '{"timestamp":'+timestamp+'}';
            jtim = '{"timestamp":'+detector.getCurrentTimeStamp()+'}';
            japp = JSON.stringify(faces[0].appearance);
            jemo = JSON.stringify(faces[0].emotions, function(key, val) {
                    return val.toFixed ? Number(val.toFixed(0)) : val;
                   });
            jexp = JSON.stringify(faces[0].expressions, function(key, val) {
                    return val.toFixed ? Number(val.toFixed(0)) : val;
                   });
            
            jres = '{'+jnom+','+jtim+','+japp+','+jemo+','+jexp+'}';
            
            document.getElementById("log_affdex").value += jres + "\n";
        }
    };
    
    if (gShowAffRes) {
        reset_aff_results();
        log('#aff_res1', "Timestamp: " + timestamp.toFixed(2) + " [s]");
        log('#aff_res1', "Number of faces: " + faces.length);
          
        if (faces.length > 0) {
            if (false) {
                log('#aff_res1', "Appearance: " + JSON.stringify(faces[0].appearance));
                log('#aff_res1', "Emotions: " + JSON.stringify(faces[0].emotions, function(key, val) {
                    return val.toFixed ? Number(val.toFixed(0)) : val;
                }));
                log('#aff_res1', "Expressions: " + JSON.stringify(faces[0].expressions, function(key, val) {
                    return val.toFixed ? Number(val.toFixed(0)) : val;
                }));
                log('#aff_res1', "Emoji: " + faces[0].emojis.dominantEmoji);
                drawFeaturePoints(image, faces[0].featurePoints);
            }
            else {
                log('#aff_res1', "");
                log('#aff_res1', "Appearance:");
                aux_str = JSON.stringify(faces[0].appearance);
                aux_str = aux_str.substring(1,aux_str.length-1);
                aux_arr = aux_str.split(",");
                for (var i in aux_arr) {
                    txt = aux_arr[i];
                    txt_arr = txt.split(":");
                    txt_arr[0] = txt_arr[0].substring(1,txt_arr[0].length-1);
                    
                    //if (txt_arr[0] == 'age'){ txt_arr[1] = "68"; }
                    
                    log('#aff_res1', "&nbsp&nbsp&nbsp&nbsp" + txt_arr[0] + ": " + txt_arr[1]);
                }
                
                log('#aff_res1', "");
                log('#aff_res1', "Emotions:");
                aux_str = JSON.stringify(faces[0].emotions, function(key, val) {
                    return val.toFixed ? Number(val.toFixed(0)) : val;
                });
                aux_str = aux_str.substring(1,aux_str.length-1);
                aux_arr = aux_str.split(",");
                for (var i in aux_arr) {
                    txt = aux_arr[i];
                    txt_arr = txt.split(":");
                    txt_arr[0] = txt_arr[0].substring(1,txt_arr[0].length-1);
                    
                    log('#aff_res1', "&nbsp&nbsp&nbsp&nbsp" + txt_arr[0] + ": " + txt_arr[1]);
                }
                
                log('#aff_res2', "");
                log('#aff_res2', "Expressions:");
                aux_str = JSON.stringify(faces[0].expressions, function(key, val) {
                    return val.toFixed ? Number(val.toFixed(0)) : val;
                });
                aux_str = aux_str.substring(1,aux_str.length-1);
                aux_arr = aux_str.split(",");
                for (var i in aux_arr) {
                    txt = aux_arr[i];
                    txt_arr = txt.split(":");
                    txt_arr[0] = txt_arr[0].substring(1,txt_arr[0].length-1);
                    
                    log('#aff_res2', "&nbsp&nbsp&nbsp&nbsp" + txt_arr[0] + ": " + txt_arr[1]);
                }
                
                log('#aff_res1', "");
                log('#aff_res1', "Emoji: " + faces[0].emojis.dominantEmoji);
                
                //drawFeaturePoints(image, faces[0].featurePoints);
            }
            
            /*
            log('#results', "Appearance: " + JSON.stringify(faces[0].appearance));
            log('#results', "Emotions: " + JSON.stringify(faces[0].emotions, function(key, val) {
                return val.toFixed ? Number(val.toFixed(0)) : val;
            }));
            log('#results', "Expressions: " + JSON.stringify(faces[0].expressions, function(key, val) {
                return val.toFixed ? Number(val.toFixed(0)) : val;
            }));
            log('#results', "Emoji: " + faces[0].emojis.dominantEmoji);
            drawFeaturePoints(image, faces[0].featurePoints);
            //*/
        }
    }
});

//Draw the detected facial feature points on the image
function drawFeaturePoints(img, featurePoints) {
    if (showPoints) {
        var contxt = $('#face_video_canvas')[0].getContext('2d');
        var hRatio = contxt.canvas.width / img.width;
        var vRatio = contxt.canvas.height / img.height;
        var ratio = Math.min(hRatio, vRatio);
        
        contxt.strokeStyle = "#FFFFFF";
        for (var id in featurePoints) {
            contxt.beginPath();
            contxt.arc(featurePoints[id].x,
            featurePoints[id].y, 2, 0, 2 * Math.PI);
            contxt.stroke();
        }
    }
}
