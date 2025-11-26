/**
 * AOLog.js
 *
 * Trend Micro Ad Blocker For Chrome 
 *
 * Created on 2022/01/19
 * Copyright 2022 Trend Micro, Inc. All rights reserved.
 *
 */
class AOLog { 
    constructor() { 
        this.CURRENT_LEVEL = "DEBUG"
        this._LEVLES = {
            OFF: 0,
            ERROR: 1,
            WARN: 2,
            INFO: 3,
            DEBUG: 4,
            VERBOSE: 5
        };
    }

    _error2String(err) { 
        return `${err.toString()}\nStack trace:\n${err.stack}`
    }

    _getLocalTimeString(date) { 
        let ONE_MINUTE_MS = 60 * 1000
        let timezoneOffSetMs = date.getTimezoneOffset() * ONE_MINUTE_MS;
        let localTime = new Date(date - timezoneOffSetMs);
        return localTime.toISOString().replace('Z', '');
    }

    _print(level, method, args) { 
        if (this._LEVLES[this.CURRENT_LEVEL] < this._LEVLES[level]) { 
            return;
        }

        if (!args || args.length === 0 || !args[0]) { 
            return;
        }

        const str = `${args[0]}`;
        args = Array.prototype.slice.call(args, 1);
        let formatted = str.replace(/{{\d+}}/g, (match, number) => { 
            if (!!args[number]) { 
                var value = args[number];
                if (value instanceof Error) {
                    value = this._error2String(value);
                } else if (value && value.message) {
                    value = value.message;
                } else if (typeof value === 'object') { 
                    value = JSON.stringify(value);
                }
            }

            return match
        })

        formatted = `${this._getLocalTimeString(new Date())}: ${formatted}`;
        console[method](formatted);
        
    }

    setLogLevel(newLevel) { 
        if (this._LEVLES[newLevel]) { 
            this.CURRENT_LEVEL = newLevel
        }
    }

    verbose(...args) { 
        this._print("VERBOSE", 'log', args);
    }

    debug(...args) { 
        this._print('DEBUG', 'debug', args);
    }

    info(...args) { 
        this._print("INFO","info", args)
    }

    warn(...args) { 
        this._print("WARN", 'warn', args);
    }

    error(...args) { 
        this._print("ERROR",'error',args)
    }


}

export default new AOLog();