(function(ext) {
    // Code to be run when the user closes the window, reloads the page, etc.    
    ext._shutdown = function() {};
    
    // Shows the status of the extension 0 = red, 1 = yellow, and 2 = green
    ext._getStatus = function() {
        return {status: 2, msg: 'Ready'};
    };
    baseUrl = "http://localhost:8085/";
    ext.connect = function (hostName, callback){
        $.ajax({
        url: baseUrl + 'connect/' + hostName,
            dataType: 'text',
            success: function (data) {
                callback();
            }
        });
    };

    ext.disconnect = function (callback) {
        $.ajax({
            url: baseUrl + 'disconnect/',
            dataType: 'text',
            success: function (data) {
                callback();
            }
        });
    };

    ext.cUp = function (angle, callback) {
        $.ajax({
            url: baseUrl + 'cUp/' + angle.toString(),
            dataType: 'text',
            success: function (data) {
                callback();
            }
        });
    };

    ext.cDown = function (angle, callback) {
        $.ajax({
            url: baseUrl + 'cDown/' + angle.toString(),
            dataType: 'text',
            success: function (data) {
                callback();
            }
        });
    };

    ext.cLeft = function (angle, callback) {
        $.ajax({
            url: baseUrl + 'cLeft/' + angle.toString(),
            dataType: 'text',
            success: function (data) {
                callback();
            }
        });
    };

    ext.cRight = function (angle, callback) {
        $.ajax({
            url: baseUrl + 'cRight/' + angle.toString(),
            dataType: 'text',
            success: function (data) {
                callback();
            }
        });
    };

    ext.centerCamera = function (callback) {
        $.ajax({
            url: baseUrl + 'centerCamera/',
            dataType: 'text',
            success: function (data) {
                callback();
            }
        });
    };

    ext.moveForward = function (speed, callback) {
        $.ajax({
            url: baseUrl + 'moveForward/' + speed.toString(),
            dataType: 'text',
            success: function (data) {
                callback();
            }
        });
    };

    ext.moveBackward = function (speed, callback) {
        $.ajax({
            url: baseUrl + 'moveBackward/' + speed.toString(),
            dataType: 'text',
            success: function (data) {
                callback();
            }
        });
    };

    ext.stop = function () {
        $.ajax({
            url: baseUrl + 'stop/',
            dataType: 'text',
            success: function (data) {
            }
        });
    };

    ext.stepForward = function (speed, duration, callback) {
        $.ajax({
            url: baseUrl + 'stepForward/' + speed.toString() + '/' + duration.toString(),
            dataType: 'text',
            success: function (data) {
                callback();
            }
        });
    };

    ext.stepBackward = function (speed, duration, callback) {
        $.ajax({
            url: baseUrl + 'stepBackward/' + speed.toString() + '/' + duration.toString(),
            dataType: 'text',
            success: function (data) {
                callback();
            }
        });
    };

    ext.turnLeft = function (angle, callback) {
        $.ajax({
            url: baseUrl + 'turnLeft/' + angle.toString(),
            dataType: 'text',
            success: function (data) {
                callback();
            }
        });
    };

    ext.turnRight = function (angle, callback) {
        $.ajax({
            url: baseUrl + 'turnRight/' + angle.toString(),
            dataType: 'text',
            success: function (data) {
                callback();
            }
        });
    };

    ext.center = function (callback) {
        $.ajax({
            url: baseUrl + 'center/',
            dataType: 'text',
            success: function (data) {
                callback();
            }
        });
    };

    ext.lightRed = function () {
        $.ajax({
            url: baseUrl + 'lightRed/',
            dataType: 'text',
            success: function (data) {
            }
        });
    };

    ext.lightGreen = function () {
        $.ajax({
            url: baseUrl + 'lightGreen/',
            dataType: 'text',
            success: function (data) {
            }
        });
    };

    ext.lightBlue = function () {
        $.ajax({
            url: baseUrl + 'lightBlue/',
            dataType: 'text',
            success: function (data) {
            }
        });
    };

    ext.buzz = function (duration) {
        setTimeout(function () {
            $.ajax({
                url: baseUrl + 'buzz/' + duration.toString(),
                dataType: 'text',
                success: function (data) {
                }
            });
        }, 10)        
    };

    ext.buzzWait = function (duration, callback) {
        $.ajax({
            url: baseUrl + 'buzz/' + duration.toString(),
            dataType: 'text',
            success: function (data) {
                callback();
            }
        });
    };

    ext.distance = function (callback) {
        $.ajax({
            url: baseUrl + 'distance/',
            dataType: 'text',
            success: function (data) {
                callback(data);
            }
        });
    };

    ext.lastError = function (callback) {
        $.ajax({
            url: baseUrl + 'lastError/',
            dataType: 'text',
            success: function (data) {
                callback(data);
            }
        });
    };

    ext.lastMessage = function (callback) {
        $.ajax({
            url: baseUrl + 'lastMessage/',
            dataType: 'text',
            success: function (data) {
                callback(data);
            }
        });
    };

    // Descriptions of the blocks and menus the extension adds
    var descriptor = {
        "blocks": [
            ["w", "Connect to %s", "connect", "piCar"],
            ["w", "Disconnect", "disconnect"],
            ["w", "Camera up %n degrees", "cUp", 10],
            ["w", "Camera down %n degrees", "cDown", 10],
            ["w", "Camera left %n degrees", "cLeft", 10],
            ["w", "Camera Right %n degrees", "cRight", 10],
            ["w", "centerCamera", "centerCamera"],
            ["w", "Move Forward at speed %n", "moveForward", 30],
            ["w", "Move Backward at speed %n", "moveBackward", 30],
            [" ", "stop", "stop"],
            ["w", "Step Forward at speed %n for %n ms", "stepForward", 30, 1000],
            ["w", "Step Backward at speed %n for %n ms", "stepBackward", 30, 1000],
            ["w", "Turn Left %n degrees", "turnLeft", 20],
            ["w", "Turn Right %n degrees", "turnRight", 20],
            ["w", "center", "center"],
            [" ", "Toggle Red light", "lightRed"],
            [" ", "Toggle Green light", "lightGreen"],
            [" ", "Toggle Blue light", "lightBlue"],
            [" ", "Buzz for %n ms", "buzz", 1000],
            ["w", "Buzz and Wait for %n ms", "buzzWait", 1000],
            ["R", "distance", "distance"],
            ["R", "lastError", "lastError"],
            ["R", "lastMessage", "lastMessage"]
        ]
    };
    // Register the extension
    ScratchExtensions.register('piCar', descriptor, ext);
})({});