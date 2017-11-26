Survey.Survey.cssType = "bootstrap";
Survey.defaultBootstrapCss.navigationButton = "btn btn-primary";

// Questions' config
var quest_wait = "Next question in...";

var quest_div1 = "<div style='min-height:150px'><h2>";
var quest_div2 = "</h2></div>";

var timer_div11 = "<div id='countdown'>";
var timer_div21 = "<div id='countdown-number_";
var timer_div22 = "' class='countdown-number'></div>";
var timer_svg11 = "<svg><circle class='svg-circle-";
var timer_svg12 = "' r='27' cx='30' cy='30'></circle></svg>";
var timer_div12 = "</div>";

// Survey
var json = {
    //showNavigationButtons: false,
    //showProgressBar: "bottom",
    //showTimerPanel: "bottom",
    //maxTimeToFinishPage: 10,
    //maxTimeToFinish: 3*(3+10)+1,
    title: "",
    pages: [
        {   name: "question_1_pre",
            questions: [{
                type: "html", name: "q1_pre",
                html: quest_div1 + quest_wait + quest_div2
                    + timer_div11 + timer_div21 + "q1_pre" + timer_div22 + timer_svg11 + "3" + timer_svg12 + timer_div12
            }]
        },
        {   name: "question_1",
            questions: [{
                type: "html", name: "q1",
                html: quest_div1 + myQuestions[0] + quest_div2
                    + timer_div11 + timer_div21 + "q1" + timer_div22 + timer_svg11 + "10" + timer_svg12 + timer_div12
            }]
        },
        {   name: "question_2_pre",
            maxTimeToFinish: 3,
            questions: [{
                type: "html", name: "q2_pre",
                html: quest_div1 + quest_wait + quest_div2
                    + timer_div11 + timer_div21 + "q2_pre" + timer_div22 + timer_svg11 + "3" + timer_svg12 + timer_div12
            }]
        },
        {   name: "question_2",
            questions: [{
                type: "html", name: "q2",
                html: quest_div1 + myQuestions[1] + quest_div2
                    + timer_div11 + timer_div21 + "q2" + timer_div22 + timer_svg11 + "10" + timer_svg12 + timer_div12
            }]
        },
        {   name: "question_3_pre",
            maxTimeToFinish: 3,
            questions: [{
                type: "html", name: "q3_pre",
                html: quest_div1 + quest_wait + quest_div2
                    + timer_div11 + timer_div21 + "q3_pre" + timer_div22 + timer_svg11 + "3" + timer_svg12 + timer_div12
            }]
        },
        {   name: "question_3",
            questions: [{
                type: "html", name: "q3",
                html: quest_div1 + myQuestions[2] + quest_div2
                    + timer_div11 + timer_div21 + "q3" + timer_div22 + timer_svg11 + "10" + timer_svg12 + timer_div12
            }]
        }
    ],
    completedHtml: "<h4>Loading...</h4>"
};

window.survey = new Survey.Model(json);

survey.onCurrentPageChanged.add(function(result, options) {
    if (options.newCurrentPage.name != survey.pages[0].name) {
        // If old page is question, write ends
        var oldname = options.oldCurrentPage.name;
        if (oldname.substring(oldname.length-4,oldname.length) != "_pre"){
            log_events_write(oldname + '_ends');
        }

        // If new page is question, write start
        var newname = options.newCurrentPage.name;
        if (newname.substring(newname.length-4,newname.length) != "_pre"){
            log_events_write(newname + '_start');
        }
    }
});

survey.onAfterRenderQuestion.add(function(surveymodel,htmlElement) {
    start_timer(surveymodel.currentPage.questions[0].name, surveymodel.currentPage.maxTimeToFinish);
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
    // Set maxTimeToFinish for each page
    for (i = 0; i < survey.pages.length; i++) {
        pagname = survey.pages[i].name;
        if (pagname.substring(pagname.length-4,pagname.length) == "_pre"){
            survey.pages[i].maxTimeToFinish = 3;
        }
        else {
            survey.pages[i].maxTimeToFinish = 10;
        }
    }

    // Start survey
    log_events_write('survey_start');

    $("#surveyElement").Survey({ 
        model: survey 
    });
}

function start_timer(question_name,question_time) {
    var eleid = 'countdown-number_' + question_name;
    var countdownNumberEl = document.getElementById(eleid);
    var countdown = question_time;
    
    countdownNumberEl.textContent = countdown;
    
    var interval = setInterval(function() {
        countdown = --countdown;// <= 0 ? 10 : countdown;
        countdownNumberEl.textContent = countdown;
        if (countdown == 0){
            clearInterval(interval);
        }
    }, 1000);
}
