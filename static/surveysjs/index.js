Survey.Survey.cssType = "bootstrap";
Survey.defaultBootstrapCss.navigationButton = "btn btn-green";

var json = {
    title: "Unleashing the true", showProgressBar: "bottom", showTimerPanel: "top", maxTimeToFinishPage: 10, maxTimeToFinish: 30,
    pages: [
        { questions: [
             { type: "comment",  name: "question1", title: "How was your first job?"}
        ]},
         { questions: [ 
            { type: "comment",  name: "question2", title: "Can you explain how amazing you find Machine Learning module?"}
         ]},
         {maxTimeToFinish: 15, questions: [
            { type: "comment",  name: "question3", title: "Is there a person you are always jelous of?"}
        ]}
    ],
    completedHtml: "<h4><p>Thank you for completing the Quiz.</p><p>You will get the result shortly...<p></h4>"
};

window.survey = new Survey.Model(json);


survey.onComplete.add(function(result) {
    document.querySelector('#surveyResult').innerHTML = "result: " + JSON.stringify(result.data);
});

survey.onComplete.add(function(survey, options){
    //send results and get the answer from the server. You may check results on the client as well, if you get the correctly answer on the client.
    var correctAnswers = {"civilwar": "1850-1900", "libertyordeath": "Patrick Henry", "magnacarta": "The foundation of the British parliamentary system"};
    setTimeout(
    function() {
        var score = 0.87;
        var total = score * 100;
        /*
        for(var key in correctAnswers) {
            var answer = survey.getValue(key);
            if(answer == correctAnswers[key]) corrected ++;
            total ++;
        }*/
        survey.completedHtml = "<h4>You sincerity score is: <b>" + score + "</b> in percentage it is <b>" + total+ "</b>%.</h4>";
        survey.render();        
    }, 3000);
});

function showSurvey() {


$("#surveyElement").Survey({ 
    model: survey 
});


}
