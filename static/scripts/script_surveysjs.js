Survey.Survey.cssType = "bootstrap";
Survey.defaultBootstrapCss.navigationButton = "btn btn-primary";

var json = {
    //title: "", showProgressBar: "bottom", showTimerPanel: "bottom", maxTimeToFinishPage: 10, maxTimeToFinish: 30,
    title: "", maxTimeToFinishPage: 10, maxTimeToFinish: 30,
    pages: [
        { questions: [
            //{ type: "comment",  name: "question1", title: myQuestions[0]}
            { type: "html", name: "question1", html: "<h2>"+myQuestions[0]+"</h2><br /><br /><br />"}
        ]
        },
        { questions: [ 
            //{ type: "comment",  name: "question2", title: myQuestions[1]}
            { type: "html", name: "question1", html: "<h2>"+myQuestions[1]+"</h2><br /><br /><br />"}
        ]
        },
        { maxTimeToFinish: 15, questions: [
            //{ type: "comment",  name: "question3", title: myQuestions[2]}
            { type: "html", name: "question1", html: "<h2>"+myQuestions[2]+"</h2><br /><br /><br />"}
        ]
        }
    ],
    completedHtml: "<h4>Loading...</h4>"
};

window.survey = new Survey.Model(json);


//survey.onComplete.add(function(result) {
//    document.querySelector('#surveyResult').innerHTML = "result: " + JSON.stringify(result.data);
//});

survey.onComplete.add(function(survey, options){
    btn_camera_stop();
    
    setTimeout(
    function() {
        document.getElementById("app_form").submit();        
    }, 1000);
    
    //send results and get the answer from the server. You may check results on the client as well, if you get the correctly answer on the client.
    //var correctAnswers = {"civilwar": "1850-1900", "libertyordeath": "Patrick Henry", "magnacarta": "The foundation of the British parliamentary system"};
    //setTimeout(
    //function() {
    //    var score = 0.87;
    //    var total = score * 100;
    //    /*
    //    for(var key in correctAnswers) {
    //        var answer = survey.getValue(key);
    //        if(answer == correctAnswers[key]) corrected ++;
    //        total ++;
    //    }*/
    //    survey.completedHtml = "<h4>You sincerity score is: <b>" + score + "</b> in percentage it is <b>" + total+ "</b>%.</h4>";
    //    survey.render();        
    //}, 3000);
});

function showSurvey() {


$("#surveyElement").Survey({ 
    model: survey 
});


}
