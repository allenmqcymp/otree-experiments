// Javascript loaded on worker.html file to dynamically inform the player
// of the payoff as he/she moves the effort slider back and forth

// BUG: when the value of the effort is a whole number eg. 1 or 2 (1 is most applicable)
// as it is used in the application; the value of the effort dicionarty is undefined for some reason

// function displayCallback() {
//     $(function() {
//         var profitMsg = "";
//         var payoff = 0;
//         var effort = $("input[name=effort]").val();
//         effort = parseFloat(effort, 10);
//         if (!effort) {
//             profitMsg = "";
//         }
//         else {
//             var costFromEffort = {{ Constants.COST_FUNCTION|json }};
//             payoff = {{ wage|json }} - costFromEffort[effort];
//             console.log(effort);
//             var costSubtract = costFromEffort[effort];
//             if (costSubtract === undefined) {
//                 console.log("experimental");
//                 console.log(costFromEffort[1.00]);
//                 console.log(costFromEffort[1]);
//                 console.log(costFromEffort[0.95]);
//             }
//             console.log(costSubtract);
//             profitMsg = payoff + " = " +  {{ wage|json }} + " - Cost( " + effort + " ) ";
//         }
//         $("p#profit-info").text(profitMsg);
//     });
// }
//
//
// $(function() {
//     $("input[name=effort]").change(function() {
//         displayCallback();
//     });
// });


var EFFORT_LEVELS = [5, 10, 15, 20, 25];
var REVENUE = 1000;
var WAGE = 700;

var config = {
  type: 'line',

};

window.onload = function() {
    var ctx = document.getElementById("canvas").getContext("2d");
    window.myChart = new Chart(ctx, config);
};