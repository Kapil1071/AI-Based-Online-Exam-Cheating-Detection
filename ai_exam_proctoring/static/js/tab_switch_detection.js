/*
----------------------------------------------------
TAB SWITCH AND WINDOW FOCUS DETECTION SCRIPT
----------------------------------------------------

This script monitors suspicious student behavior during the exam.

Events detected:

1. Tab switching
2. Window focus loss
3. Page visibility change

Each event is sent to the backend API:
POST /log_event
*/


// Get session ID from hidden HTML input
const sessionIdElement = document.getElementById("session_id")

let sessionId = null

if(sessionIdElement){

    sessionId = sessionIdElement.value

}



/*
----------------------------------------------------
FUNCTION TO SEND EVENT TO BACKEND
----------------------------------------------------
*/

function sendCheatingEvent(eventType){

    if(!sessionId) return

    fetch("/log_event",{

        method: "POST",

        headers:{
            "Content-Type":"application/json"
        },

        body: JSON.stringify({
            session_id: sessionId,
            event_type: eventType
        })

    })
}



/*
----------------------------------------------------
TAB SWITCH DETECTION
----------------------------------------------------

The Page Visibility API detects when the page
becomes hidden (user switches tab).
*/

document.addEventListener("visibilitychange", function(){

    if(document.hidden){

        console.log("Tab switch detected")

        sendCheatingEvent("Tab Switch")

    }

})



/*
----------------------------------------------------
WINDOW FOCUS LOSS DETECTION
----------------------------------------------------

Triggers when the browser window loses focus.

Examples:
- User switches application
- User minimizes browser
- User opens another window
*/

window.addEventListener("blur", function(){

    console.log("Window focus lost")

    sendCheatingEvent("Window Focus Lost")

})



/*
----------------------------------------------------
OPTIONAL: COPY PASTE DETECTION
----------------------------------------------------

Students copying content from the exam page
can also be logged as suspicious behavior.
*/

document.addEventListener("copy", function(){

    console.log("Copy attempt detected")

    sendCheatingEvent("Copy Attempt")

})