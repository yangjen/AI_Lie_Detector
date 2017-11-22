Survey.Survey.cssType = "bootstrap";
Survey.defaultBootstrapCss.navigationButton = "btn btn-primary";

var html_quest_pre = "<div style='min-height:150px'><h2>"
var html_quest_post = "</h2></div>"
var html_timer_pre = "<div id='countdown'><div id='countdown-number_"
var html_timer_post = "' class='countdown-number'></div><svg><circle r='27' cx='30' cy='30'></circle></svg></div>"

var json = {
    //showProgressBar: "bottom",
    //showTimerPanel: "bottom",
    maxTimeToFinishPage: 10,
    maxTimeToFinish: 30,
    title: "",
    pages: [
        { name: "question_1", 
          questions: [
            //{ type: "comment",  name: "question_1", title: myQuestions[0]}
            { type: "html", name: "q1", html: html_quest_pre+myQuestions[0]+html_quest_post + html_timer_pre+'q1'+html_timer_post}
        ]
        },
        { name: "question_2",
          questions: [
            { type: "html", name: "q2", html: html_quest_pre+myQuestions[1]+html_quest_post + html_timer_pre+'q2'+html_timer_post}
        ]
        },
        { name: "question_3",
          questions: [
            { type: "html", name: "q3", html: html_quest_pre+myQuestions[2]+html_quest_post + html_timer_pre+'q3'+html_timer_post}
        ]
        }
    ],
    completedHtml: "<h4>Loading...</h4>"
};

window.survey = new Survey.Model(json);

survey.onCurrentPageChanged.add(function(result, options) {
    log_events_write(options.newCurrentPage.name + '_start');
});

survey.onAfterRenderQuestion.add(function(surveymodel,htmlElement) {
    start_timer(surveymodel.currentPage.questions[0].name);
})

//survey.onComplete.add(function(result) {
//    document.querySelector('#surveyResult').innerHTML = "result: " + JSON.stringify(result.data);
//});

survey.onComplete.add(function(survey, options){
    log_events_write('survey_end');
    
    camera_stop();
    
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
    log_events_write('survey_start');
    $("#surveyElement").Survey({ 
        model: survey 
    });
}

function start_timer(question_name) {
    var eleid = 'countdown-number_' + question_name;
    var countdownNumberEl = document.getElementById(eleid);
    var countdown = 10;
    
    countdownNumberEl.textContent = countdown;
    
    var interval = setInterval(function() {
        countdown = --countdown;// <= 0 ? 10 : countdown;
        countdownNumberEl.textContent = countdown;
        if (countdown == 0){
            clearInterval(interval);
        }
    }, 1000);
}
