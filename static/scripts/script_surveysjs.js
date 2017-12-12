Survey.Survey.cssType = "bootstrap";
Survey.defaultBootstrapCss.navigationButton = "btn btn-primary";

// Questions' config
var quest_div1 = "<div style='min-height:150px'><h2>";
var quest_div2 = "</h2></div>";

var timer_div11 = "<div id='countdown'>";
var timer_div21 = "<div id='countdown-number_";
var timer_div22 = "' class='countdown-number'></div>";
var timer_svg11 = "<svg>";
var timer_svg20 = "<circle class='svg-circle-w' r='45' cx='50' cy='50'></circle>";
var timer_svg30 = "<circle class='svg-circle-a' r='30' cx='50' cy='50'></circle>";
var timer_svg12 = "</svg>";
var timer_div12 = "</div>";

var comment_wait = "Get ready....";
var comment_answ = "Go!";
var comment_div = "<div><center><h3 id='comment'>" + comment_wait + "</h3></center></div>";

// Survey
var json = {
    showNavigationButtons: false,
    //showProgressBar: "bottom",
    //showTimerPanel: "bottom",
    //maxTimeToFinishPage: 3+10,
    maxTimeToFinish: 3*(3+10)+1,
    title: "",
    pages: [
        {   name: "question_1",
            questions: [{
                type: "html", name: "q1",
                html: quest_div1 + myQuestions[0] + quest_div2
                    + timer_div11
                    + timer_div21 + "q1" + timer_div22
                    + timer_svg11 + timer_svg20 + timer_svg30 + timer_svg12
                    + timer_div12
                    + comment_div
            }]
        },
        {   name: "question_2",
            questions: [{
                type: "html", name: "q2",
                html: quest_div1 + myQuestions[1] + quest_div2
                    + timer_div11
                    + timer_div21 + "q2" + timer_div22
                    + timer_svg11 + timer_svg20 + timer_svg30 + timer_svg12
                    + timer_div12
                    + comment_div
            }]
        },
        {   name: "question_3",
            questions: [{
                type: "html", name: "q3",
                html: quest_div1 + myQuestions[2] + quest_div2
                    + timer_div11
                    + timer_div21 + "q3" + timer_div22
                    + timer_svg11 + timer_svg20 + timer_svg30 + timer_svg12
                    + timer_div12
                    + comment_div
            }]
        }
    ],
    completedHtml: "<h4>Analyzing your responses...</h4>"
};

window.survey = new Survey.Model(json);

survey.onCurrentPageChanged.add(function(result, options) {
    if (options.newCurrentPage.name != survey.pages[0].name) {
        // If old page is question, write ends
        var oldname = options.oldCurrentPage.name;
        if (oldname.substring(oldname.length-4,oldname.length) != "_pre"){
            log_events_write(oldname + '_ends');
        }
    }
});

survey.onAfterRenderQuestion.add(function(surveymodel,htmlElement) {
    start_timer(surveymodel.currentPage.questions[0].name);
})

//survey.onComplete.add(function(result) {
//    document.querySelector('#surveyResult').innerHTML = "result: " + JSON.stringify(result.data);
//});

survey.onComplete.add(function(survey, options){
    log_events_write('question_3_ends');
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
    // Start survey
    log_events_write('survey_start');

    $("#surveyElement").Survey({ 
        model: survey 
    });
}

function start_timer(question_name) {
    var eleid = 'comment';
    var commentEl = document.getElementById(eleid);
    var eleid = 'countdown-number_' + question_name;
    var countdownNumberEl = document.getElementById(eleid);

    var this_waiting = true;
    var this_isLastPage = survey.isLastPage;
    var this_currentPageNo = survey.currentPageNo;

    var countdown = 3;
    countdownNumberEl.textContent = countdown;
    var interval = setInterval(function() {
        if (this_currentPageNo != survey.currentPageNo) {
            clearInterval(interval);
        };
        countdown = --countdown;
        if (countdown == 0){
            if (this_waiting) {
                this_waiting = false;
                countdown = 10;
                log_events_write(survey.currentPage.name + '_start');
                commentEl.textContent = comment_answ;
            }
            else {
                if (this_isLastPage) {
                    survey.doComplete();
                }
                else {
                    survey.nextPage()
                };
                clearInterval(interval);
            }
        }
        countdownNumberEl.textContent = countdown;
    }, 1000);
}
