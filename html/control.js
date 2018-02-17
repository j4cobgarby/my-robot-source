var ws;
var l_down = false;
var u_down = false;
var r_down = false;
var d_down = false;

function init() {
    ws = new WebSocket("ws://192.168.0.57:1337/");

    ws.onoopen = function() {
        // on open conn
    }

    ws.onmessage = function(e) {
        // when received message
        // e is recv'd string
    }

    ws.onclose = function() {
        // on close conn
    }

    ws.onerror = function(e) {
        // error
    }
}

function set_appropriate_motion() {
    if (u_down && !d_down && !r_down && !l_down) {
        ws.send("motor1_fd");
        ws.send("motor2_fd");
    }
    if (d_down && !l_down && !r_down) {
        ws.send("motor1_bk");
        ws.send("motor2_bk");
    }
    if (!u_down && !d_down && !l_down && !r_down) {
        ws.send("motor1_hlt");
        ws.send("motor2_hlt");
    }
    if (l_down && !r_down) {
        console.log("L");
        ws.send("motor2_bk");
        if (!u_down && !d_down) ws.send("motor1_fd");
    }
    if (r_down && !l_down) {
        ws.send("motor1_bk");
        if (!u_down && !d_down) ws.send("motor2_fd");
    }
}

function initkbd() {		
    document.body.onkeydown = function(e) {
        if (e.keyCode == 37) l_down = true;
        if (e.keyCode == 38) u_down = true;
        if (e.keyCode == 39) r_down = true;
        if (e.keyCode == 40) d_down = true;
        if (e.keyCode == 32) ws.send("led_test");
        set_appropriate_motion();
    }
    document.body.onkeyup   = function(e) {
        if (e.keyCode == 37) l_down = false;
        if (e.keyCode == 38) u_down = false;
        if (e.keyCode == 39) r_down = false;
        if (e.keyCode == 40) d_down = false;
        set_appropriate_motion();
    }
}
