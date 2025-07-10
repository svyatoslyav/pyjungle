function getCurrentScore() {
    return localStorage.getItem("score") ? parseInt(localStorage.getItem("score")) : 0;
}
function updateScore() {
    const score = getCurrentScore();
    document.getElementById("counter").innerText = score;
    localStorage.setItem("score", score);
}
document.getElementById("clickButton").addEventListener("click", function() {
    let score = getCurrentScore();
    score += 1;
    localStorage.setItem("score", score);
    updateScore();
    if(localStorage.getItem("score") > 15){
        document.body.style.backgroundColor = "#00FFFF";
}
});
window.onload = updateScore;
if(localStorage.getItem("score") > 15){
    document.body.style.backgroundColor = "#00FFFF";
}
document.getElementById("resetButton").addEventListener("click", function() {
    let score = getCurrentScore();
    score = 0
    localStorage.setItem("score", score);
    updateScore();
    document.body.style.backgroundColor = "#FFFFFF";
})

