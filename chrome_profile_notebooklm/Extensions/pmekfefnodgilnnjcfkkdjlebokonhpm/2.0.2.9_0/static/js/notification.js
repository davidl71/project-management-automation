$("#clickProceed").on("click", () => {
    window.parent.postMessage({
        "cmd": "closeNotificationWithOK"
    },"*")
})

$("#clickCancel").on("click", () => {
    window.parent.postMessage({
        "cmd":"closeNotificationWithCancel"
    },"*")
})