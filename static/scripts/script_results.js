// Set text inside the buttons
document.getElementById("btn_res_1").textContent = myQuestions[0];
document.getElementById("btn_res_2").textContent = myQuestions[1];
document.getElementById("btn_res_3").textContent = myQuestions[2];

// Change the class of the button with the lying question
document.getElementById("btn_res_" + myEstimate).className = "btn btn-warning";

// Variable que revisa si ya se entrego resultado
var user_clicked = false;

function btn_result_click(clicked_id) {
    if (!user_clicked) {
        var btnEl = document.getElementById(clicked_id);

        document.getElementById("res_ask").style.display = "none";

        // Correct prediction
        if (btnEl.className == "btn btn-warning"){
            btnEl.className = "btn btn-success";
            document.getElementById("res_comment").textContent = ":)";
        }
        // Wrong prediction
        else {
            btnEl.className = "btn btn-success";
            document.getElementById("btn_res_" + myEstimate).className = "btn btn-danger";
            document.getElementById("res_comment").textContent = ":(";
        };

        // Send the new label to the python
        $("#log_res").html(clicked_id.substring(clicked_id.length-1,clicked_id.length));
        setTimeout(
            function() {
                document.getElementById("res_form").submit();
            }, 1000);

        user_clicked = true;
    };
};
