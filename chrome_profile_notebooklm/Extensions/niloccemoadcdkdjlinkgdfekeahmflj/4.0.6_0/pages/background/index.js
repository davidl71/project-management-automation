import { _ as __extends$2, a as getGlobalObject, c as checkOrSetAlreadyCaught, l as logger, i as isPrimitive, S as SessionStatus, b as SyncPromise, u as uuid4, d as dateTimestampInSeconds, e as Scope, n as normalize, t as truncate, f as isThenable, h as isPlainObject, j as addGlobalEventProcessor, k as getEventDescription, m as isMatchingPattern, p as parseRetryAfterHeader, o as isErrorEvent, q as isString, r as getLocationHref, s as getCurrentHub, v as safeJoin, w as htmlTreeAsString, x as parseUrl, y as isInstanceOf, z as timestampWithMs, A as dropUndefinedKeys, B as setDefaultIcon, O as OPEN_OPTIONS, C as OPEN_POCKET, D as COLOR_MODE_CHANGE, E as SEND_TAG_ERROR, T as TAGS_SYNC, R as RESAVE_ITEM, F as REMOVE_ITEM, L as LOGGED_OUT_OF_POCKET, U as USER_LOG_IN, G as AUTH_CODE_RECEIVED, H as addExceptionMechanism, I as isDOMError, J as isDOMException, K as addExceptionTypeValue, M as isError, N as isEvent, P as SAVE_TO_POCKET_REQUEST, g as getSetting, Q as SAVE_TO_POCKET_SUCCESS, V as SAVE_TO_POCKET_FAILURE, W as REMOVE_ITEM_REQUEST, X as setToolbarIcon, Y as TAG_SYNC_REQUEST, Z as UPDATE_TAG_ERROR, $ as setSettings, a0 as withScope, a1 as Hub, a2 as isNodeEnv, a3 as fill, a4 as extractExceptionKeysForMessage, a5 as normalizeToSize, a6 as getFunctionName, a7 as UPDATE_ITEM_PREVIEW, a8 as UPDATE_STORED_TAGS, a9 as SUGGESTED_TAGS_SUCCESS, aa as REMOVE_ITEM_SUCCESS, ab as REMOVE_ITEM_FAILURE, ac as TAG_SYNC_SUCCESS, ad as TAG_SYNC_FAILURE, ae as getMainCarrier, af as loadModule, ag as __read$3, ah as __values$2, ai as __assign$3, aj as urlEncode, ak as captureMessage, al as dynamicRequire, am as captureException } from '../../chunks/actions-639cd34d.js';
import { i as isSystemPage, a as isSystemLink, c as closeLoginPage, g as getAccessToken, d as deriveItemData } from '../../chunks/helpers-10be1fb3.js';
import { A as API_URL, L as LOGOUT_URL, a as AUTH_URL, P as POCKET_LIST, b as POCKET_HOME, C as CONSUMER_KEY } from '../../chunks/constants-064bdc7d.js';

/*! *****************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */
/* global Reflect, Promise */

var extendStatics$1 = function(d, b) {
    extendStatics$1 = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return extendStatics$1(d, b);
};

function __extends$1(d, b) {
    extendStatics$1(d, b);
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
}

var __assign$2 = function() {
    __assign$2 = Object.assign || function __assign(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p)) t[p] = s[p];
        }
        return t;
    };
    return __assign$2.apply(this, arguments);
};

function __values$1(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
}

function __read$2(o, n) {
    var m = typeof Symbol === "function" && o[Symbol.iterator];
    if (!m) return o;
    var i = m.call(o), r, ar = [], e;
    try {
        while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
    }
    catch (error) { e = { error: error }; }
    finally {
        try {
            if (r && !r.done && (m = i["return"])) m.call(i);
        }
        finally { if (e) throw e.error; }
    }
    return ar;
}

function __spread$2() {
    for (var ar = [], i = 0; i < arguments.length; i++)
        ar = ar.concat(__read$2(arguments[i]));
    return ar;
}

/** JSDoc */
// eslint-disable-next-line import/export
var Severity;
(function (Severity) {
    /** JSDoc */
    Severity["Fatal"] = "fatal";
    /** JSDoc */
    Severity["Error"] = "error";
    /** JSDoc */
    Severity["Warning"] = "warning";
    /** JSDoc */
    Severity["Log"] = "log";
    /** JSDoc */
    Severity["Info"] = "info";
    /** JSDoc */
    Severity["Debug"] = "debug";
    /** JSDoc */
    Severity["Critical"] = "critical";
})(Severity || (Severity = {}));
// eslint-disable-next-line @typescript-eslint/no-namespace, import/export
(function (Severity) {
    /**
     * Converts a string-based level into a {@link Severity}.
     *
     * @param level string representation of Severity
     * @returns Severity
     */
    function fromString(level) {
        switch (level) {
            case 'debug':
                return Severity.Debug;
            case 'info':
                return Severity.Info;
            case 'warn':
            case 'warning':
                return Severity.Warning;
            case 'error':
                return Severity.Error;
            case 'fatal':
                return Severity.Fatal;
            case 'critical':
                return Severity.Critical;
            case 'log':
            default:
                return Severity.Log;
        }
    }
    Severity.fromString = fromString;
})(Severity || (Severity = {}));

/** The status of an event. */
// eslint-disable-next-line import/export
var Status;
(function (Status) {
    /** The status could not be determined. */
    Status["Unknown"] = "unknown";
    /** The event was skipped due to configuration or callbacks. */
    Status["Skipped"] = "skipped";
    /** The event was sent to Sentry successfully. */
    Status["Success"] = "success";
    /** The client is currently rate limited and will try again later. */
    Status["RateLimit"] = "rate_limit";
    /** The event could not be processed. */
    Status["Invalid"] = "invalid";
    /** A server-side error occurred during submission. */
    Status["Failed"] = "failed";
})(Status || (Status = {}));
// eslint-disable-next-line @typescript-eslint/no-namespace, import/export
(function (Status) {
    /**
     * Converts a HTTP status code into a {@link Status}.
     *
     * @param code The HTTP response status code.
     * @returns The send status or {@link Status.Unknown}.
     */
    function fromHttpCode(code) {
        if (code >= 200 && code < 300) {
            return Status.Success;
        }
        if (code === 429) {
            return Status.RateLimit;
        }
        if (code >= 400 && code < 500) {
            return Status.Invalid;
        }
        if (code >= 500) {
            return Status.Failed;
        }
        return Status.Unknown;
    }
    Status.fromHttpCode = fromHttpCode;
})(Status || (Status = {}));

var TransactionSamplingMethod;
(function (TransactionSamplingMethod) {
    TransactionSamplingMethod["Explicit"] = "explicitly_set";
    TransactionSamplingMethod["Sampler"] = "client_sampler";
    TransactionSamplingMethod["Rate"] = "client_rate";
    TransactionSamplingMethod["Inheritance"] = "inheritance";
})(TransactionSamplingMethod || (TransactionSamplingMethod = {}));

var Outcome;
(function (Outcome) {
    Outcome["BeforeSend"] = "before_send";
    Outcome["EventProcessor"] = "event_processor";
    Outcome["NetworkError"] = "network_error";
    Outcome["QueueOverflow"] = "queue_overflow";
    Outcome["RateLimitBackoff"] = "ratelimit_backoff";
    Outcome["SampleRate"] = "sample_rate";
})(Outcome || (Outcome = {}));

/**
 * Consumes the promise and logs the error when it rejects.
 * @param promise A promise to forget.
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function forget(promise) {
    void promise.then(null, function (e) {
        // TODO: Use a better logging mechanism
        // eslint-disable-next-line no-console
        console.error(e);
    });
}

var setPrototypeOf = Object.setPrototypeOf || ({ __proto__: [] } instanceof Array ? setProtoOf : mixinProperties);
/**
 * setPrototypeOf polyfill using __proto__
 */
// eslint-disable-next-line @typescript-eslint/ban-types
function setProtoOf(obj, proto) {
    // @ts-ignore __proto__ does not exist on obj
    obj.__proto__ = proto;
    return obj;
}
/**
 * setPrototypeOf polyfill using mixin
 */
// eslint-disable-next-line @typescript-eslint/ban-types
function mixinProperties(obj, proto) {
    for (var prop in proto) {
        if (!Object.prototype.hasOwnProperty.call(obj, prop)) {
            // @ts-ignore typescript complains about indexing so we remove
            obj[prop] = proto[prop];
        }
    }
    return obj;
}

/** An error emitted by Sentry SDKs and related utilities. */
var SentryError = /** @class */ (function (_super) {
    __extends$2(SentryError, _super);
    function SentryError(message) {
        var _newTarget = this.constructor;
        var _this = _super.call(this, message) || this;
        _this.message = message;
        _this.name = _newTarget.prototype.constructor.name;
        setPrototypeOf(_this, _newTarget.prototype);
        return _this;
    }
    return SentryError;
}(Error));

/** Regular expression used to parse a Dsn. */
var DSN_REGEX = /^(?:(\w+):)\/\/(?:(\w+)(?::(\w+))?@)([\w.-]+)(?::(\d+))?\/(.+)/;
/** Error message */
var ERROR_MESSAGE = 'Invalid Dsn';
/** The Sentry Dsn, identifying a Sentry instance and project. */
var Dsn = /** @class */ (function () {
    /** Creates a new Dsn component */
    function Dsn(from) {
        if (typeof from === 'string') {
            this._fromString(from);
        }
        else {
            this._fromComponents(from);
        }
        this._validate();
    }
    /**
     * Renders the string representation of this Dsn.
     *
     * By default, this will render the public representation without the password
     * component. To get the deprecated private representation, set `withPassword`
     * to true.
     *
     * @param withPassword When set to true, the password will be included.
     */
    Dsn.prototype.toString = function (withPassword) {
        if (withPassword === void 0) { withPassword = false; }
        var _a = this, host = _a.host, path = _a.path, pass = _a.pass, port = _a.port, projectId = _a.projectId, protocol = _a.protocol, publicKey = _a.publicKey;
        return (protocol + "://" + publicKey + (withPassword && pass ? ":" + pass : '') +
            ("@" + host + (port ? ":" + port : '') + "/" + (path ? path + "/" : path) + projectId));
    };
    /** Parses a string into this Dsn. */
    Dsn.prototype._fromString = function (str) {
        var match = DSN_REGEX.exec(str);
        if (!match) {
            throw new SentryError(ERROR_MESSAGE);
        }
        var _a = __read$3(match.slice(1), 6), protocol = _a[0], publicKey = _a[1], _b = _a[2], pass = _b === void 0 ? '' : _b, host = _a[3], _c = _a[4], port = _c === void 0 ? '' : _c, lastPath = _a[5];
        var path = '';
        var projectId = lastPath;
        var split = projectId.split('/');
        if (split.length > 1) {
            path = split.slice(0, -1).join('/');
            projectId = split.pop();
        }
        if (projectId) {
            var projectMatch = projectId.match(/^\d+/);
            if (projectMatch) {
                projectId = projectMatch[0];
            }
        }
        this._fromComponents({ host: host, pass: pass, path: path, projectId: projectId, port: port, protocol: protocol, publicKey: publicKey });
    };
    /** Maps Dsn components into this instance. */
    Dsn.prototype._fromComponents = function (components) {
        // TODO this is for backwards compatibility, and can be removed in a future version
        if ('user' in components && !('publicKey' in components)) {
            components.publicKey = components.user;
        }
        this.user = components.publicKey || '';
        this.protocol = components.protocol;
        this.publicKey = components.publicKey || '';
        this.pass = components.pass || '';
        this.host = components.host;
        this.port = components.port || '';
        this.path = components.path || '';
        this.projectId = components.projectId;
    };
    /** Validates this Dsn and throws on error. */
    Dsn.prototype._validate = function () {
        var _this = this;
        ['protocol', 'publicKey', 'host', 'projectId'].forEach(function (component) {
            if (!_this[component]) {
                throw new SentryError(ERROR_MESSAGE + ": " + component + " missing");
            }
        });
        if (!this.projectId.match(/^\d+$/)) {
            throw new SentryError(ERROR_MESSAGE + ": Invalid projectId " + this.projectId);
        }
        if (this.protocol !== 'http' && this.protocol !== 'https') {
            throw new SentryError(ERROR_MESSAGE + ": Invalid protocol " + this.protocol);
        }
        if (this.port && isNaN(parseInt(this.port, 10))) {
            throw new SentryError(ERROR_MESSAGE + ": Invalid port " + this.port);
        }
    };
    return Dsn;
}());

/**
 * Tells whether current environment supports Fetch API
 * {@link supportsFetch}.
 *
 * @returns Answer to the given question.
 */
function supportsFetch() {
    if (!('fetch' in getGlobalObject())) {
        return false;
    }
    try {
        new Headers();
        new Request('');
        new Response();
        return true;
    }
    catch (e) {
        return false;
    }
}
/**
 * isNativeFetch checks if the given function is a native implementation of fetch()
 */
// eslint-disable-next-line @typescript-eslint/ban-types
function isNativeFetch(func) {
    return func && /^function fetch\(\)\s+\{\s+\[native code\]\s+\}$/.test(func.toString());
}
/**
 * Tells whether current environment supports Fetch API natively
 * {@link supportsNativeFetch}.
 *
 * @returns true if `window.fetch` is natively implemented, false otherwise
 */
function supportsNativeFetch() {
    if (!supportsFetch()) {
        return false;
    }
    var global = getGlobalObject();
    // Fast path to avoid DOM I/O
    // eslint-disable-next-line @typescript-eslint/unbound-method
    if (isNativeFetch(global.fetch)) {
        return true;
    }
    // window.fetch is implemented, but is polyfilled or already wrapped (e.g: by a chrome extension)
    // so create a "pure" iframe to see if that has native fetch
    var result = false;
    var doc = global.document;
    // eslint-disable-next-line deprecation/deprecation
    if (doc && typeof doc.createElement === "function") {
        try {
            var sandbox = doc.createElement('iframe');
            sandbox.hidden = true;
            doc.head.appendChild(sandbox);
            if (sandbox.contentWindow && sandbox.contentWindow.fetch) {
                // eslint-disable-next-line @typescript-eslint/unbound-method
                result = isNativeFetch(sandbox.contentWindow.fetch);
            }
            doc.head.removeChild(sandbox);
        }
        catch (err) {
            logger.warn('Could not create sandbox iframe for pure fetch check, bailing to window.fetch: ', err);
        }
    }
    return result;
}
/**
 * Tells whether current environment supports Referrer Policy API
 * {@link supportsReferrerPolicy}.
 *
 * @returns Answer to the given question.
 */
function supportsReferrerPolicy() {
    // Despite all stars in the sky saying that Edge supports old draft syntax, aka 'never', 'always', 'origin' and 'default
    // https://caniuse.com/#feat=referrer-policy
    // It doesn't. And it throw exception instead of ignoring this parameter...
    // REF: https://github.com/getsentry/raven-js/issues/1233
    if (!supportsFetch()) {
        return false;
    }
    try {
        new Request('_', {
            referrerPolicy: 'origin',
        });
        return true;
    }
    catch (e) {
        return false;
    }
}
/**
 * Tells whether current environment supports History API
 * {@link supportsHistory}.
 *
 * @returns Answer to the given question.
 */
function supportsHistory() {
    // NOTE: in Chrome App environment, touching history.pushState, *even inside
    //       a try/catch block*, will cause Chrome to output an error to console.error
    // borrowed from: https://github.com/angular/angular.js/pull/13945/files
    var global = getGlobalObject();
    /* eslint-disable @typescript-eslint/no-unsafe-member-access */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    var chrome = global.chrome;
    var isChromePackagedApp = chrome && chrome.app && chrome.app.runtime;
    /* eslint-enable @typescript-eslint/no-unsafe-member-access */
    var hasHistoryApi = 'history' in global && !!global.history.pushState && !!global.history.replaceState;
    return !isChromePackagedApp && hasHistoryApi;
}

var global$4 = getGlobalObject();
/**
 * Instrument native APIs to call handlers that can be used to create breadcrumbs, APM spans etc.
 *  - Console API
 *  - Fetch API
 *  - XHR API
 *  - History API
 *  - DOM API (click/typing)
 *  - Error API
 *  - UnhandledRejection API
 */
var handlers = {};
var instrumented = {};
/** Instruments given API */
function instrument(type) {
    if (instrumented[type]) {
        return;
    }
    instrumented[type] = true;
    switch (type) {
        case 'console':
            instrumentConsole();
            break;
        case 'dom':
            instrumentDOM();
            break;
        case 'xhr':
            instrumentXHR();
            break;
        case 'fetch':
            instrumentFetch();
            break;
        case 'history':
            instrumentHistory();
            break;
        case 'error':
            instrumentError();
            break;
        case 'unhandledrejection':
            instrumentUnhandledRejection();
            break;
        default:
            logger.warn('unknown instrumentation type:', type);
    }
}
/**
 * Add handler that will be called when given type of instrumentation triggers.
 * Use at your own risk, this might break without changelog notice, only used internally.
 * @hidden
 */
function addInstrumentationHandler(handler) {
    if (!handler || typeof handler.type !== 'string' || typeof handler.callback !== 'function') {
        return;
    }
    handlers[handler.type] = handlers[handler.type] || [];
    handlers[handler.type].push(handler.callback);
    instrument(handler.type);
}
/** JSDoc */
function triggerHandlers(type, data) {
    var e_1, _a;
    if (!type || !handlers[type]) {
        return;
    }
    try {
        for (var _b = __values$2(handlers[type] || []), _c = _b.next(); !_c.done; _c = _b.next()) {
            var handler = _c.value;
            try {
                handler(data);
            }
            catch (e) {
                logger.error("Error while triggering instrumentation handler.\nType: " + type + "\nName: " + getFunctionName(handler) + "\nError: " + e);
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
        }
        finally { if (e_1) throw e_1.error; }
    }
}
/** JSDoc */
function instrumentConsole() {
    if (!('console' in global$4)) {
        return;
    }
    ['debug', 'info', 'warn', 'error', 'log', 'assert'].forEach(function (level) {
        if (!(level in global$4.console)) {
            return;
        }
        fill(global$4.console, level, function (originalConsoleLevel) {
            return function () {
                var args = [];
                for (var _i = 0; _i < arguments.length; _i++) {
                    args[_i] = arguments[_i];
                }
                triggerHandlers('console', { args: args, level: level });
                // this fails for some browsers. :(
                if (originalConsoleLevel) {
                    Function.prototype.apply.call(originalConsoleLevel, global$4.console, args);
                }
            };
        });
    });
}
/** JSDoc */
function instrumentFetch() {
    if (!supportsNativeFetch()) {
        return;
    }
    fill(global$4, 'fetch', function (originalFetch) {
        return function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var handlerData = {
                args: args,
                fetchData: {
                    method: getFetchMethod(args),
                    url: getFetchUrl(args),
                },
                startTimestamp: Date.now(),
            };
            triggerHandlers('fetch', __assign$3({}, handlerData));
            // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
            return originalFetch.apply(global$4, args).then(function (response) {
                triggerHandlers('fetch', __assign$3(__assign$3({}, handlerData), { endTimestamp: Date.now(), response: response }));
                return response;
            }, function (error) {
                triggerHandlers('fetch', __assign$3(__assign$3({}, handlerData), { endTimestamp: Date.now(), error: error }));
                // NOTE: If you are a Sentry user, and you are seeing this stack frame,
                //       it means the sentry.javascript SDK caught an error invoking your application code.
                //       This is expected behavior and NOT indicative of a bug with sentry.javascript.
                throw error;
            });
        };
    });
}
/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/** Extract `method` from fetch call arguments */
function getFetchMethod(fetchArgs) {
    if (fetchArgs === void 0) { fetchArgs = []; }
    if ('Request' in global$4 && isInstanceOf(fetchArgs[0], Request) && fetchArgs[0].method) {
        return String(fetchArgs[0].method).toUpperCase();
    }
    if (fetchArgs[1] && fetchArgs[1].method) {
        return String(fetchArgs[1].method).toUpperCase();
    }
    return 'GET';
}
/** Extract `url` from fetch call arguments */
function getFetchUrl(fetchArgs) {
    if (fetchArgs === void 0) { fetchArgs = []; }
    if (typeof fetchArgs[0] === 'string') {
        return fetchArgs[0];
    }
    if ('Request' in global$4 && isInstanceOf(fetchArgs[0], Request)) {
        return fetchArgs[0].url;
    }
    return String(fetchArgs[0]);
}
/* eslint-enable @typescript-eslint/no-unsafe-member-access */
/** JSDoc */
function instrumentXHR() {
    if (!('XMLHttpRequest' in global$4)) {
        return;
    }
    // Poor man's implementation of ES6 `Map`, tracking and keeping in sync key and value separately.
    var requestKeys = [];
    var requestValues = [];
    var xhrproto = XMLHttpRequest.prototype;
    fill(xhrproto, 'open', function (originalOpen) {
        return function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            // eslint-disable-next-line @typescript-eslint/no-this-alias
            var xhr = this;
            var url = args[1];
            xhr.__sentry_xhr__ = {
                // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
                method: isString(args[0]) ? args[0].toUpperCase() : args[0],
                url: args[1],
            };
            // if Sentry key appears in URL, don't capture it as a request
            // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
            if (isString(url) && xhr.__sentry_xhr__.method === 'POST' && url.match(/sentry_key/)) {
                xhr.__sentry_own_request__ = true;
            }
            var onreadystatechangeHandler = function () {
                if (xhr.readyState === 4) {
                    try {
                        // touching statusCode in some platforms throws
                        // an exception
                        if (xhr.__sentry_xhr__) {
                            xhr.__sentry_xhr__.status_code = xhr.status;
                        }
                    }
                    catch (e) {
                        /* do nothing */
                    }
                    try {
                        var requestPos = requestKeys.indexOf(xhr);
                        if (requestPos !== -1) {
                            // Make sure to pop both key and value to keep it in sync.
                            requestKeys.splice(requestPos);
                            var args_1 = requestValues.splice(requestPos)[0];
                            if (xhr.__sentry_xhr__ && args_1[0] !== undefined) {
                                xhr.__sentry_xhr__.body = args_1[0];
                            }
                        }
                    }
                    catch (e) {
                        /* do nothing */
                    }
                    triggerHandlers('xhr', {
                        args: args,
                        endTimestamp: Date.now(),
                        startTimestamp: Date.now(),
                        xhr: xhr,
                    });
                }
            };
            if ('onreadystatechange' in xhr && typeof xhr.onreadystatechange === 'function') {
                fill(xhr, 'onreadystatechange', function (original) {
                    return function () {
                        var readyStateArgs = [];
                        for (var _i = 0; _i < arguments.length; _i++) {
                            readyStateArgs[_i] = arguments[_i];
                        }
                        onreadystatechangeHandler();
                        return original.apply(xhr, readyStateArgs);
                    };
                });
            }
            else {
                xhr.addEventListener('readystatechange', onreadystatechangeHandler);
            }
            return originalOpen.apply(xhr, args);
        };
    });
    fill(xhrproto, 'send', function (originalSend) {
        return function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            requestKeys.push(this);
            requestValues.push(args);
            triggerHandlers('xhr', {
                args: args,
                startTimestamp: Date.now(),
                xhr: this,
            });
            return originalSend.apply(this, args);
        };
    });
}
var lastHref;
/** JSDoc */
function instrumentHistory() {
    if (!supportsHistory()) {
        return;
    }
    var oldOnPopState = global$4.onpopstate;
    global$4.onpopstate = function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        var to = global$4.location.href;
        // keep track of the current URL state, as we always receive only the updated state
        var from = lastHref;
        lastHref = to;
        triggerHandlers('history', {
            from: from,
            to: to,
        });
        if (oldOnPopState) {
            // Apparently this can throw in Firefox when incorrectly implemented plugin is installed.
            // https://github.com/getsentry/sentry-javascript/issues/3344
            // https://github.com/bugsnag/bugsnag-js/issues/469
            try {
                return oldOnPopState.apply(this, args);
            }
            catch (_oO) {
                // no-empty
            }
        }
    };
    /** @hidden */
    function historyReplacementFunction(originalHistoryFunction) {
        return function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var url = args.length > 2 ? args[2] : undefined;
            if (url) {
                // coerce to string (this is what pushState does)
                var from = lastHref;
                var to = String(url);
                // keep track of the current URL state, as we always receive only the updated state
                lastHref = to;
                triggerHandlers('history', {
                    from: from,
                    to: to,
                });
            }
            return originalHistoryFunction.apply(this, args);
        };
    }
    fill(global$4.history, 'pushState', historyReplacementFunction);
    fill(global$4.history, 'replaceState', historyReplacementFunction);
}
var debounceDuration = 1000;
var debounceTimerID;
var lastCapturedEvent;
/**
 * Decide whether the current event should finish the debounce of previously captured one.
 * @param previous previously captured event
 * @param current event to be captured
 */
function shouldShortcircuitPreviousDebounce(previous, current) {
    // If there was no previous event, it should always be swapped for the new one.
    if (!previous) {
        return true;
    }
    // If both events have different type, then user definitely performed two separate actions. e.g. click + keypress.
    if (previous.type !== current.type) {
        return true;
    }
    try {
        // If both events have the same type, it's still possible that actions were performed on different targets.
        // e.g. 2 clicks on different buttons.
        if (previous.target !== current.target) {
            return true;
        }
    }
    catch (e) {
        // just accessing `target` property can throw an exception in some rare circumstances
        // see: https://github.com/getsentry/sentry-javascript/issues/838
    }
    // If both events have the same type _and_ same `target` (an element which triggered an event, _not necessarily_
    // to which an event listener was attached), we treat them as the same action, as we want to capture
    // only one breadcrumb. e.g. multiple clicks on the same button, or typing inside a user input box.
    return false;
}
/**
 * Decide whether an event should be captured.
 * @param event event to be captured
 */
function shouldSkipDOMEvent(event) {
    // We are only interested in filtering `keypress` events for now.
    if (event.type !== 'keypress') {
        return false;
    }
    try {
        var target = event.target;
        if (!target || !target.tagName) {
            return true;
        }
        // Only consider keypress events on actual input elements. This will disregard keypresses targeting body
        // e.g.tabbing through elements, hotkeys, etc.
        if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable) {
            return false;
        }
    }
    catch (e) {
        // just accessing `target` property can throw an exception in some rare circumstances
        // see: https://github.com/getsentry/sentry-javascript/issues/838
    }
    return true;
}
/**
 * Wraps addEventListener to capture UI breadcrumbs
 * @param handler function that will be triggered
 * @param globalListener indicates whether event was captured by the global event listener
 * @returns wrapped breadcrumb events handler
 * @hidden
 */
function makeDOMEventHandler(handler, globalListener) {
    if (globalListener === void 0) { globalListener = false; }
    return function (event) {
        // It's possible this handler might trigger multiple times for the same
        // event (e.g. event propagation through node ancestors).
        // Ignore if we've already captured that event.
        if (!event || lastCapturedEvent === event) {
            return;
        }
        // We always want to skip _some_ events.
        if (shouldSkipDOMEvent(event)) {
            return;
        }
        var name = event.type === 'keypress' ? 'input' : event.type;
        // If there is no debounce timer, it means that we can safely capture the new event and store it for future comparisons.
        if (debounceTimerID === undefined) {
            handler({
                event: event,
                name: name,
                global: globalListener,
            });
            lastCapturedEvent = event;
        }
        // If there is a debounce awaiting, see if the new event is different enough to treat it as a unique one.
        // If that's the case, emit the previous event and store locally the newly-captured DOM event.
        else if (shouldShortcircuitPreviousDebounce(lastCapturedEvent, event)) {
            handler({
                event: event,
                name: name,
                global: globalListener,
            });
            lastCapturedEvent = event;
        }
        // Start a new debounce timer that will prevent us from capturing multiple events that should be grouped together.
        clearTimeout(debounceTimerID);
        debounceTimerID = global$4.setTimeout(function () {
            debounceTimerID = undefined;
        }, debounceDuration);
    };
}
/** JSDoc */
function instrumentDOM() {
    if (!('document' in global$4)) {
        return;
    }
    // Make it so that any click or keypress that is unhandled / bubbled up all the way to the document triggers our dom
    // handlers. (Normally we have only one, which captures a breadcrumb for each click or keypress.) Do this before
    // we instrument `addEventListener` so that we don't end up attaching this handler twice.
    var triggerDOMHandler = triggerHandlers.bind(null, 'dom');
    var globalDOMEventHandler = makeDOMEventHandler(triggerDOMHandler, true);
    global$4.document.addEventListener('click', globalDOMEventHandler, false);
    global$4.document.addEventListener('keypress', globalDOMEventHandler, false);
    // After hooking into click and keypress events bubbled up to `document`, we also hook into user-handled
    // clicks & keypresses, by adding an event listener of our own to any element to which they add a listener. That
    // way, whenever one of their handlers is triggered, ours will be, too. (This is needed because their handler
    // could potentially prevent the event from bubbling up to our global listeners. This way, our handler are still
    // guaranteed to fire at least once.)
    ['EventTarget', 'Node'].forEach(function (target) {
        // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
        var proto = global$4[target] && global$4[target].prototype;
        // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access, no-prototype-builtins
        if (!proto || !proto.hasOwnProperty || !proto.hasOwnProperty('addEventListener')) {
            return;
        }
        fill(proto, 'addEventListener', function (originalAddEventListener) {
            return function (type, listener, options) {
                if (type === 'click' || type == 'keypress') {
                    try {
                        var el = this;
                        var handlers_1 = (el.__sentry_instrumentation_handlers__ = el.__sentry_instrumentation_handlers__ || {});
                        var handlerForType = (handlers_1[type] = handlers_1[type] || { refCount: 0 });
                        if (!handlerForType.handler) {
                            var handler = makeDOMEventHandler(triggerDOMHandler);
                            handlerForType.handler = handler;
                            originalAddEventListener.call(this, type, handler, options);
                        }
                        handlerForType.refCount += 1;
                    }
                    catch (e) {
                        // Accessing dom properties is always fragile.
                        // Also allows us to skip `addEventListenrs` calls with no proper `this` context.
                    }
                }
                return originalAddEventListener.call(this, type, listener, options);
            };
        });
        fill(proto, 'removeEventListener', function (originalRemoveEventListener) {
            return function (type, listener, options) {
                if (type === 'click' || type == 'keypress') {
                    try {
                        var el = this;
                        var handlers_2 = el.__sentry_instrumentation_handlers__ || {};
                        var handlerForType = handlers_2[type];
                        if (handlerForType) {
                            handlerForType.refCount -= 1;
                            // If there are no longer any custom handlers of the current type on this element, we can remove ours, too.
                            if (handlerForType.refCount <= 0) {
                                originalRemoveEventListener.call(this, type, handlerForType.handler, options);
                                handlerForType.handler = undefined;
                                delete handlers_2[type]; // eslint-disable-line @typescript-eslint/no-dynamic-delete
                            }
                            // If there are no longer any custom handlers of any type on this element, cleanup everything.
                            if (Object.keys(handlers_2).length === 0) {
                                delete el.__sentry_instrumentation_handlers__;
                            }
                        }
                    }
                    catch (e) {
                        // Accessing dom properties is always fragile.
                        // Also allows us to skip `addEventListenrs` calls with no proper `this` context.
                    }
                }
                return originalRemoveEventListener.call(this, type, listener, options);
            };
        });
    });
}
var _oldOnErrorHandler = null;
/** JSDoc */
function instrumentError() {
    _oldOnErrorHandler = global$4.onerror;
    global$4.onerror = function (msg, url, line, column, error) {
        triggerHandlers('error', {
            column: column,
            error: error,
            line: line,
            msg: msg,
            url: url,
        });
        if (_oldOnErrorHandler) {
            // eslint-disable-next-line prefer-rest-params
            return _oldOnErrorHandler.apply(this, arguments);
        }
        return false;
    };
}
var _oldOnUnhandledRejectionHandler = null;
/** JSDoc */
function instrumentUnhandledRejection() {
    _oldOnUnhandledRejectionHandler = global$4.onunhandledrejection;
    global$4.onunhandledrejection = function (e) {
        triggerHandlers('unhandledrejection', e);
        if (_oldOnUnhandledRejectionHandler) {
            // eslint-disable-next-line prefer-rest-params
            return _oldOnUnhandledRejectionHandler.apply(this, arguments);
        }
        return true;
    };
}

/** A simple queue that holds promises. */
var PromiseBuffer = /** @class */ (function () {
    function PromiseBuffer(_limit) {
        this._limit = _limit;
        /** Internal set of queued Promises */
        this._buffer = [];
    }
    /**
     * Says if the buffer is ready to take more requests
     */
    PromiseBuffer.prototype.isReady = function () {
        return this._limit === undefined || this.length() < this._limit;
    };
    /**
     * Add a promise (representing an in-flight action) to the queue, and set it to remove itself on fulfillment.
     *
     * @param taskProducer A function producing any PromiseLike<T>; In previous versions this used to be `task:
     *        PromiseLike<T>`, but under that model, Promises were instantly created on the call-site and their executor
     *        functions therefore ran immediately. Thus, even if the buffer was full, the action still happened. By
     *        requiring the promise to be wrapped in a function, we can defer promise creation until after the buffer
     *        limit check.
     * @returns The original promise.
     */
    PromiseBuffer.prototype.add = function (taskProducer) {
        var _this = this;
        if (!this.isReady()) {
            return SyncPromise.reject(new SentryError('Not adding Promise due to buffer limit reached.'));
        }
        // start the task and add its promise to the queue
        var task = taskProducer();
        if (this._buffer.indexOf(task) === -1) {
            this._buffer.push(task);
        }
        void task
            .then(function () { return _this.remove(task); })
            // Use `then(null, rejectionHandler)` rather than `catch(rejectionHandler)` so that we can use `PromiseLike`
            // rather than `Promise`. `PromiseLike` doesn't have a `.catch` method, making its polyfill smaller. (ES5 didn't
            // have promises, so TS has to polyfill when down-compiling.)
            .then(null, function () {
            return _this.remove(task).then(null, function () {
                // We have to add another catch here because `this.remove()` starts a new promise chain.
            });
        });
        return task;
    };
    /**
     * Remove a promise from the queue.
     *
     * @param task Can be any PromiseLike<T>
     * @returns Removed promise.
     */
    PromiseBuffer.prototype.remove = function (task) {
        var removedTask = this._buffer.splice(this._buffer.indexOf(task), 1)[0];
        return removedTask;
    };
    /**
     * This function returns the number of unresolved promises in the queue.
     */
    PromiseBuffer.prototype.length = function () {
        return this._buffer.length;
    };
    /**
     * Wait for all promises in the queue to resolve or for timeout to expire, whichever comes first.
     *
     * @param timeout The time, in ms, after which to resolve to `false` if the queue is still non-empty. Passing `0` (or
     * not passing anything) will make the promise wait as long as it takes for the queue to drain before resolving to
     * `true`.
     * @returns A promise which will resolve to `true` if the queue is already empty or drains before the timeout, and
     * `false` otherwise
     */
    PromiseBuffer.prototype.drain = function (timeout) {
        var _this = this;
        return new SyncPromise(function (resolve) {
            // wait for `timeout` ms and then resolve to `false` (if not cancelled first)
            var capturedSetTimeout = setTimeout(function () {
                if (timeout && timeout > 0) {
                    resolve(false);
                }
            }, timeout);
            // if all promises resolve in time, cancel the timer and resolve to `true`
            void SyncPromise.all(_this._buffer)
                .then(function () {
                clearTimeout(capturedSetTimeout);
                resolve(true);
            })
                .then(null, function () {
                resolve(true);
            });
        });
    };
    return PromiseBuffer;
}());

var SENTRY_API_VERSION = '7';
/**
 * Helper class to provide urls, headers and metadata that can be used to form
 * different types of requests to Sentry endpoints.
 * Supports both envelopes and regular event requests.
 **/
var API = /** @class */ (function () {
    /** Create a new instance of API */
    function API(dsn, metadata, tunnel) {
        if (metadata === void 0) { metadata = {}; }
        this.dsn = dsn;
        this._dsnObject = new Dsn(dsn);
        this.metadata = metadata;
        this._tunnel = tunnel;
    }
    /** Returns the Dsn object. */
    API.prototype.getDsn = function () {
        return this._dsnObject;
    };
    /** Does this transport force envelopes? */
    API.prototype.forceEnvelope = function () {
        return !!this._tunnel;
    };
    /** Returns the prefix to construct Sentry ingestion API endpoints. */
    API.prototype.getBaseApiEndpoint = function () {
        var dsn = this.getDsn();
        var protocol = dsn.protocol ? dsn.protocol + ":" : '';
        var port = dsn.port ? ":" + dsn.port : '';
        return protocol + "//" + dsn.host + port + (dsn.path ? "/" + dsn.path : '') + "/api/";
    };
    /** Returns the store endpoint URL. */
    API.prototype.getStoreEndpoint = function () {
        return this._getIngestEndpoint('store');
    };
    /**
     * Returns the store endpoint URL with auth in the query string.
     *
     * Sending auth as part of the query string and not as custom HTTP headers avoids CORS preflight requests.
     */
    API.prototype.getStoreEndpointWithUrlEncodedAuth = function () {
        return this.getStoreEndpoint() + "?" + this._encodedAuth();
    };
    /**
     * Returns the envelope endpoint URL with auth in the query string.
     *
     * Sending auth as part of the query string and not as custom HTTP headers avoids CORS preflight requests.
     */
    API.prototype.getEnvelopeEndpointWithUrlEncodedAuth = function () {
        if (this.forceEnvelope()) {
            return this._tunnel;
        }
        return this._getEnvelopeEndpoint() + "?" + this._encodedAuth();
    };
    /** Returns only the path component for the store endpoint. */
    API.prototype.getStoreEndpointPath = function () {
        var dsn = this.getDsn();
        return (dsn.path ? "/" + dsn.path : '') + "/api/" + dsn.projectId + "/store/";
    };
    /**
     * Returns an object that can be used in request headers.
     * This is needed for node and the old /store endpoint in sentry
     */
    API.prototype.getRequestHeaders = function (clientName, clientVersion) {
        // CHANGE THIS to use metadata but keep clientName and clientVersion compatible
        var dsn = this.getDsn();
        var header = ["Sentry sentry_version=" + SENTRY_API_VERSION];
        header.push("sentry_client=" + clientName + "/" + clientVersion);
        header.push("sentry_key=" + dsn.publicKey);
        if (dsn.pass) {
            header.push("sentry_secret=" + dsn.pass);
        }
        return {
            'Content-Type': 'application/json',
            'X-Sentry-Auth': header.join(', '),
        };
    };
    /** Returns the url to the report dialog endpoint. */
    API.prototype.getReportDialogEndpoint = function (dialogOptions) {
        if (dialogOptions === void 0) { dialogOptions = {}; }
        var dsn = this.getDsn();
        var endpoint = this.getBaseApiEndpoint() + "embed/error-page/";
        var encodedOptions = [];
        encodedOptions.push("dsn=" + dsn.toString());
        for (var key in dialogOptions) {
            if (key === 'dsn') {
                continue;
            }
            if (key === 'user') {
                if (!dialogOptions.user) {
                    continue;
                }
                if (dialogOptions.user.name) {
                    encodedOptions.push("name=" + encodeURIComponent(dialogOptions.user.name));
                }
                if (dialogOptions.user.email) {
                    encodedOptions.push("email=" + encodeURIComponent(dialogOptions.user.email));
                }
            }
            else {
                encodedOptions.push(encodeURIComponent(key) + "=" + encodeURIComponent(dialogOptions[key]));
            }
        }
        if (encodedOptions.length) {
            return endpoint + "?" + encodedOptions.join('&');
        }
        return endpoint;
    };
    /** Returns the envelope endpoint URL. */
    API.prototype._getEnvelopeEndpoint = function () {
        return this._getIngestEndpoint('envelope');
    };
    /** Returns the ingest API endpoint for target. */
    API.prototype._getIngestEndpoint = function (target) {
        if (this._tunnel) {
            return this._tunnel;
        }
        var base = this.getBaseApiEndpoint();
        var dsn = this.getDsn();
        return "" + base + dsn.projectId + "/" + target + "/";
    };
    /** Returns a URL-encoded string with auth config suitable for a query string. */
    API.prototype._encodedAuth = function () {
        var dsn = this.getDsn();
        var auth = {
            // We send only the minimum set of required information. See
            // https://github.com/getsentry/sentry-javascript/issues/2572.
            sentry_key: dsn.publicKey,
            sentry_version: SENTRY_API_VERSION,
        };
        return urlEncode(auth);
    };
    return API;
}());

/*! *****************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */

var __assign$1 = function() {
    __assign$1 = Object.assign || function __assign(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p)) t[p] = s[p];
        }
        return t;
    };
    return __assign$1.apply(this, arguments);
};

function __rest(s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
}

function __values(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
}

function __read$1(o, n) {
    var m = typeof Symbol === "function" && o[Symbol.iterator];
    if (!m) return o;
    var i = m.call(o), r, ar = [], e;
    try {
        while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
    }
    catch (error) { e = { error: error }; }
    finally {
        try {
            if (r && !r.done && (m = i["return"])) m.call(i);
        }
        finally { if (e) throw e.error; }
    }
    return ar;
}

function __spread$1() {
    for (var ar = [], i = 0; i < arguments.length; i++)
        ar = ar.concat(__read$1(arguments[i]));
    return ar;
}

var installedIntegrations = [];
/**
 * @private
 */
function filterDuplicates(integrations) {
    return integrations.reduce(function (acc, integrations) {
        if (acc.every(function (accIntegration) { return integrations.name !== accIntegration.name; })) {
            acc.push(integrations);
        }
        return acc;
    }, []);
}
/** Gets integration to install */
function getIntegrationsToSetup(options) {
    var defaultIntegrations = (options.defaultIntegrations && __spread$1(options.defaultIntegrations)) || [];
    var userIntegrations = options.integrations;
    var integrations = __spread$1(filterDuplicates(defaultIntegrations));
    if (Array.isArray(userIntegrations)) {
        // Filter out integrations that are also included in user options
        integrations = __spread$1(integrations.filter(function (integrations) {
            return userIntegrations.every(function (userIntegration) { return userIntegration.name !== integrations.name; });
        }), filterDuplicates(userIntegrations));
    }
    else if (typeof userIntegrations === 'function') {
        integrations = userIntegrations(integrations);
        integrations = Array.isArray(integrations) ? integrations : [integrations];
    }
    // Make sure that if present, `Debug` integration will always run last
    var integrationsNames = integrations.map(function (i) { return i.name; });
    var alwaysLastToRun = 'Debug';
    if (integrationsNames.indexOf(alwaysLastToRun) !== -1) {
        integrations.push.apply(integrations, __spread$1(integrations.splice(integrationsNames.indexOf(alwaysLastToRun), 1)));
    }
    return integrations;
}
/** Setup given integration */
function setupIntegration(integration) {
    if (installedIntegrations.indexOf(integration.name) !== -1) {
        return;
    }
    integration.setupOnce(addGlobalEventProcessor, getCurrentHub);
    installedIntegrations.push(integration.name);
    logger.log("Integration installed: " + integration.name);
}
/**
 * Given a list of integration instances this installs them all. When `withDefaults` is set to `true` then all default
 * integrations are added unless they were already provided before.
 * @param integrations array of integration instances
 * @param withDefault should enable default integrations
 */
function setupIntegrations(options) {
    var integrations = {};
    getIntegrationsToSetup(options).forEach(function (integration) {
        integrations[integration.name] = integration;
        setupIntegration(integration);
    });
    // set the `initialized` flag so we don't run through the process again unecessarily; use `Object.defineProperty`
    // because by default it creates a property which is nonenumerable, which we want since `initialized` shouldn't be
    // considered a member of the index the way the actual integrations are
    Object.defineProperty(integrations, 'initialized', { value: true });
    return integrations;
}

var ALREADY_SEEN_ERROR = "Not capturing exception because it's already been captured.";
/**
 * Base implementation for all JavaScript SDK clients.
 *
 * Call the constructor with the corresponding backend constructor and options
 * specific to the client subclass. To access these options later, use
 * {@link Client.getOptions}. Also, the Backend instance is available via
 * {@link Client.getBackend}.
 *
 * If a Dsn is specified in the options, it will be parsed and stored. Use
 * {@link Client.getDsn} to retrieve the Dsn at any moment. In case the Dsn is
 * invalid, the constructor will throw a {@link SentryException}. Note that
 * without a valid Dsn, the SDK will not send any events to Sentry.
 *
 * Before sending an event via the backend, it is passed through
 * {@link BaseClient._prepareEvent} to add SDK information and scope data
 * (breadcrumbs and context). To add more custom information, override this
 * method and extend the resulting prepared event.
 *
 * To issue automatically created events (e.g. via instrumentation), use
 * {@link Client.captureEvent}. It will prepare the event and pass it through
 * the callback lifecycle. To issue auto-breadcrumbs, use
 * {@link Client.addBreadcrumb}.
 *
 * @example
 * class NodeClient extends BaseClient<NodeBackend, NodeOptions> {
 *   public constructor(options: NodeOptions) {
 *     super(NodeBackend, options);
 *   }
 *
 *   // ...
 * }
 */
var BaseClient = /** @class */ (function () {
    /**
     * Initializes this client instance.
     *
     * @param backendClass A constructor function to create the backend.
     * @param options Options for the client.
     */
    function BaseClient(backendClass, options) {
        /** Array of used integrations. */
        this._integrations = {};
        /** Number of calls being processed */
        this._numProcessing = 0;
        this._backend = new backendClass(options);
        this._options = options;
        if (options.dsn) {
            this._dsn = new Dsn(options.dsn);
        }
    }
    /**
     * @inheritDoc
     */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/explicit-module-boundary-types
    BaseClient.prototype.captureException = function (exception, hint, scope) {
        var _this = this;
        // ensure we haven't captured this very object before
        if (checkOrSetAlreadyCaught(exception)) {
            logger.log(ALREADY_SEEN_ERROR);
            return;
        }
        var eventId = hint && hint.event_id;
        this._process(this._getBackend()
            .eventFromException(exception, hint)
            .then(function (event) { return _this._captureEvent(event, hint, scope); })
            .then(function (result) {
            eventId = result;
        }));
        return eventId;
    };
    /**
     * @inheritDoc
     */
    BaseClient.prototype.captureMessage = function (message, level, hint, scope) {
        var _this = this;
        var eventId = hint && hint.event_id;
        var promisedEvent = isPrimitive(message)
            ? this._getBackend().eventFromMessage(String(message), level, hint)
            : this._getBackend().eventFromException(message, hint);
        this._process(promisedEvent
            .then(function (event) { return _this._captureEvent(event, hint, scope); })
            .then(function (result) {
            eventId = result;
        }));
        return eventId;
    };
    /**
     * @inheritDoc
     */
    BaseClient.prototype.captureEvent = function (event, hint, scope) {
        var _a;
        // ensure we haven't captured this very object before
        if (((_a = hint) === null || _a === void 0 ? void 0 : _a.originalException) && checkOrSetAlreadyCaught(hint.originalException)) {
            logger.log(ALREADY_SEEN_ERROR);
            return;
        }
        var eventId = hint && hint.event_id;
        this._process(this._captureEvent(event, hint, scope).then(function (result) {
            eventId = result;
        }));
        return eventId;
    };
    /**
     * @inheritDoc
     */
    BaseClient.prototype.captureSession = function (session) {
        if (!this._isEnabled()) {
            logger.warn('SDK not enabled, will not capture session.');
            return;
        }
        if (!(typeof session.release === 'string')) {
            logger.warn('Discarded session because of missing or non-string release');
        }
        else {
            this._sendSession(session);
            // After sending, we set init false to indicate it's not the first occurrence
            session.update({ init: false });
        }
    };
    /**
     * @inheritDoc
     */
    BaseClient.prototype.getDsn = function () {
        return this._dsn;
    };
    /**
     * @inheritDoc
     */
    BaseClient.prototype.getOptions = function () {
        return this._options;
    };
    /**
     * @inheritDoc
     */
    BaseClient.prototype.getTransport = function () {
        return this._getBackend().getTransport();
    };
    /**
     * @inheritDoc
     */
    BaseClient.prototype.flush = function (timeout) {
        var _this = this;
        return this._isClientDoneProcessing(timeout).then(function (clientFinished) {
            return _this.getTransport()
                .close(timeout)
                .then(function (transportFlushed) { return clientFinished && transportFlushed; });
        });
    };
    /**
     * @inheritDoc
     */
    BaseClient.prototype.close = function (timeout) {
        var _this = this;
        return this.flush(timeout).then(function (result) {
            _this.getOptions().enabled = false;
            return result;
        });
    };
    /**
     * Sets up the integrations
     */
    BaseClient.prototype.setupIntegrations = function () {
        if (this._isEnabled() && !this._integrations.initialized) {
            this._integrations = setupIntegrations(this._options);
        }
    };
    /**
     * @inheritDoc
     */
    BaseClient.prototype.getIntegration = function (integration) {
        try {
            return this._integrations[integration.id] || null;
        }
        catch (_oO) {
            logger.warn("Cannot retrieve integration " + integration.id + " from the current Client");
            return null;
        }
    };
    /** Updates existing session based on the provided event */
    BaseClient.prototype._updateSessionFromEvent = function (session, event) {
        var e_1, _a;
        var crashed = false;
        var errored = false;
        var exceptions = event.exception && event.exception.values;
        if (exceptions) {
            errored = true;
            try {
                for (var exceptions_1 = __values(exceptions), exceptions_1_1 = exceptions_1.next(); !exceptions_1_1.done; exceptions_1_1 = exceptions_1.next()) {
                    var ex = exceptions_1_1.value;
                    var mechanism = ex.mechanism;
                    if (mechanism && mechanism.handled === false) {
                        crashed = true;
                        break;
                    }
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (exceptions_1_1 && !exceptions_1_1.done && (_a = exceptions_1.return)) _a.call(exceptions_1);
                }
                finally { if (e_1) throw e_1.error; }
            }
        }
        // A session is updated and that session update is sent in only one of the two following scenarios:
        // 1. Session with non terminal status and 0 errors + an error occurred -> Will set error count to 1 and send update
        // 2. Session with non terminal status and 1 error + a crash occurred -> Will set status crashed and send update
        var sessionNonTerminal = session.status === SessionStatus.Ok;
        var shouldUpdateAndSend = (sessionNonTerminal && session.errors === 0) || (sessionNonTerminal && crashed);
        if (shouldUpdateAndSend) {
            session.update(__assign$1(__assign$1({}, (crashed && { status: SessionStatus.Crashed })), { errors: session.errors || Number(errored || crashed) }));
            this.captureSession(session);
        }
    };
    /** Deliver captured session to Sentry */
    BaseClient.prototype._sendSession = function (session) {
        this._getBackend().sendSession(session);
    };
    /**
     * Determine if the client is finished processing. Returns a promise because it will wait `timeout` ms before saying
     * "no" (resolving to `false`) in order to give the client a chance to potentially finish first.
     *
     * @param timeout The time, in ms, after which to resolve to `false` if the client is still busy. Passing `0` (or not
     * passing anything) will make the promise wait as long as it takes for processing to finish before resolving to
     * `true`.
     * @returns A promise which will resolve to `true` if processing is already done or finishes before the timeout, and
     * `false` otherwise
     */
    BaseClient.prototype._isClientDoneProcessing = function (timeout) {
        var _this = this;
        return new SyncPromise(function (resolve) {
            var ticked = 0;
            var tick = 1;
            var interval = setInterval(function () {
                if (_this._numProcessing == 0) {
                    clearInterval(interval);
                    resolve(true);
                }
                else {
                    ticked += tick;
                    if (timeout && ticked >= timeout) {
                        clearInterval(interval);
                        resolve(false);
                    }
                }
            }, tick);
        });
    };
    /** Returns the current backend. */
    BaseClient.prototype._getBackend = function () {
        return this._backend;
    };
    /** Determines whether this SDK is enabled and a valid Dsn is present. */
    BaseClient.prototype._isEnabled = function () {
        return this.getOptions().enabled !== false && this._dsn !== undefined;
    };
    /**
     * Adds common information to events.
     *
     * The information includes release and environment from `options`,
     * breadcrumbs and context (extra, tags and user) from the scope.
     *
     * Information that is already present in the event is never overwritten. For
     * nested objects, such as the context, keys are merged.
     *
     * @param event The original event.
     * @param hint May contain additional information about the original exception.
     * @param scope A scope containing event metadata.
     * @returns A new event with more information.
     */
    BaseClient.prototype._prepareEvent = function (event, scope, hint) {
        var _this = this;
        var _a = this.getOptions().normalizeDepth, normalizeDepth = _a === void 0 ? 3 : _a;
        var prepared = __assign$1(__assign$1({}, event), { event_id: event.event_id || (hint && hint.event_id ? hint.event_id : uuid4()), timestamp: event.timestamp || dateTimestampInSeconds() });
        this._applyClientOptions(prepared);
        this._applyIntegrationsMetadata(prepared);
        // If we have scope given to us, use it as the base for further modifications.
        // This allows us to prevent unnecessary copying of data if `captureContext` is not provided.
        var finalScope = scope;
        if (hint && hint.captureContext) {
            finalScope = Scope.clone(finalScope).update(hint.captureContext);
        }
        // We prepare the result here with a resolved Event.
        var result = SyncPromise.resolve(prepared);
        // This should be the last thing called, since we want that
        // {@link Hub.addEventProcessor} gets the finished prepared event.
        if (finalScope) {
            // In case we have a hub we reassign it.
            result = finalScope.applyToEvent(prepared, hint);
        }
        return result.then(function (evt) {
            if (typeof normalizeDepth === 'number' && normalizeDepth > 0) {
                return _this._normalizeEvent(evt, normalizeDepth);
            }
            return evt;
        });
    };
    /**
     * Applies `normalize` function on necessary `Event` attributes to make them safe for serialization.
     * Normalized keys:
     * - `breadcrumbs.data`
     * - `user`
     * - `contexts`
     * - `extra`
     * @param event Event
     * @returns Normalized event
     */
    BaseClient.prototype._normalizeEvent = function (event, depth) {
        if (!event) {
            return null;
        }
        var normalized = __assign$1(__assign$1(__assign$1(__assign$1(__assign$1({}, event), (event.breadcrumbs && {
            breadcrumbs: event.breadcrumbs.map(function (b) { return (__assign$1(__assign$1({}, b), (b.data && {
                data: normalize(b.data, depth),
            }))); }),
        })), (event.user && {
            user: normalize(event.user, depth),
        })), (event.contexts && {
            contexts: normalize(event.contexts, depth),
        })), (event.extra && {
            extra: normalize(event.extra, depth),
        }));
        // event.contexts.trace stores information about a Transaction. Similarly,
        // event.spans[] stores information about child Spans. Given that a
        // Transaction is conceptually a Span, normalization should apply to both
        // Transactions and Spans consistently.
        // For now the decision is to skip normalization of Transactions and Spans,
        // so this block overwrites the normalized event to add back the original
        // Transaction information prior to normalization.
        if (event.contexts && event.contexts.trace) {
            // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
            normalized.contexts.trace = event.contexts.trace;
        }
        var _a = this.getOptions()._experiments, _experiments = _a === void 0 ? {} : _a;
        if (_experiments.ensureNoCircularStructures) {
            return normalize(normalized);
        }
        return normalized;
    };
    /**
     *  Enhances event using the client configuration.
     *  It takes care of all "static" values like environment, release and `dist`,
     *  as well as truncating overly long values.
     * @param event event instance to be enhanced
     */
    BaseClient.prototype._applyClientOptions = function (event) {
        var options = this.getOptions();
        var environment = options.environment, release = options.release, dist = options.dist, _a = options.maxValueLength, maxValueLength = _a === void 0 ? 250 : _a;
        if (!('environment' in event)) {
            event.environment = 'environment' in options ? environment : 'production';
        }
        if (event.release === undefined && release !== undefined) {
            event.release = release;
        }
        if (event.dist === undefined && dist !== undefined) {
            event.dist = dist;
        }
        if (event.message) {
            event.message = truncate(event.message, maxValueLength);
        }
        var exception = event.exception && event.exception.values && event.exception.values[0];
        if (exception && exception.value) {
            exception.value = truncate(exception.value, maxValueLength);
        }
        var request = event.request;
        if (request && request.url) {
            request.url = truncate(request.url, maxValueLength);
        }
    };
    /**
     * This function adds all used integrations to the SDK info in the event.
     * @param event The event that will be filled with all integrations.
     */
    BaseClient.prototype._applyIntegrationsMetadata = function (event) {
        var integrationsArray = Object.keys(this._integrations);
        if (integrationsArray.length > 0) {
            event.sdk = event.sdk || {};
            event.sdk.integrations = __spread$1((event.sdk.integrations || []), integrationsArray);
        }
    };
    /**
     * Tells the backend to send this event
     * @param event The Sentry event to send
     */
    BaseClient.prototype._sendEvent = function (event) {
        this._getBackend().sendEvent(event);
    };
    /**
     * Processes the event and logs an error in case of rejection
     * @param event
     * @param hint
     * @param scope
     */
    BaseClient.prototype._captureEvent = function (event, hint, scope) {
        return this._processEvent(event, hint, scope).then(function (finalEvent) {
            return finalEvent.event_id;
        }, function (reason) {
            logger.error(reason);
            return undefined;
        });
    };
    /**
     * Processes an event (either error or message) and sends it to Sentry.
     *
     * This also adds breadcrumbs and context information to the event. However,
     * platform specific meta data (such as the User's IP address) must be added
     * by the SDK implementor.
     *
     *
     * @param event The event to send to Sentry.
     * @param hint May contain additional information about the original exception.
     * @param scope A scope containing event metadata.
     * @returns A SyncPromise that resolves with the event or rejects in case event was/will not be send.
     */
    BaseClient.prototype._processEvent = function (event, hint, scope) {
        var _this = this;
        var _a, _b;
        // eslint-disable-next-line @typescript-eslint/unbound-method
        var _c = this.getOptions(), beforeSend = _c.beforeSend, sampleRate = _c.sampleRate;
        var transport = this.getTransport();
        if (!this._isEnabled()) {
            return SyncPromise.reject(new SentryError('SDK not enabled, will not capture event.'));
        }
        var isTransaction = event.type === 'transaction';
        // 1.0 === 100% events are sent
        // 0.0 === 0% events are sent
        // Sampling for transaction happens somewhere else
        if (!isTransaction && typeof sampleRate === 'number' && Math.random() > sampleRate) {
            (_b = (_a = transport).recordLostEvent) === null || _b === void 0 ? void 0 : _b.call(_a, Outcome.SampleRate, 'event');
            return SyncPromise.reject(new SentryError("Discarding event because it's not included in the random sample (sampling rate = " + sampleRate + ")"));
        }
        return this._prepareEvent(event, scope, hint)
            .then(function (prepared) {
            var _a, _b;
            if (prepared === null) {
                (_b = (_a = transport).recordLostEvent) === null || _b === void 0 ? void 0 : _b.call(_a, Outcome.EventProcessor, event.type || 'event');
                throw new SentryError('An event processor returned null, will not send event.');
            }
            var isInternalException = hint && hint.data && hint.data.__sentry__ === true;
            if (isInternalException || isTransaction || !beforeSend) {
                return prepared;
            }
            var beforeSendResult = beforeSend(prepared, hint);
            return _this._ensureBeforeSendRv(beforeSendResult);
        })
            .then(function (processedEvent) {
            var _a, _b;
            if (processedEvent === null) {
                (_b = (_a = transport).recordLostEvent) === null || _b === void 0 ? void 0 : _b.call(_a, Outcome.BeforeSend, event.type || 'event');
                throw new SentryError('`beforeSend` returned `null`, will not send event.');
            }
            var session = scope && scope.getSession && scope.getSession();
            if (!isTransaction && session) {
                _this._updateSessionFromEvent(session, processedEvent);
            }
            _this._sendEvent(processedEvent);
            return processedEvent;
        })
            .then(null, function (reason) {
            if (reason instanceof SentryError) {
                throw reason;
            }
            _this.captureException(reason, {
                data: {
                    __sentry__: true,
                },
                originalException: reason,
            });
            throw new SentryError("Event processing pipeline threw an error, original event will not be sent. Details have been sent as a new event.\nReason: " + reason);
        });
    };
    /**
     * Occupies the client with processing and event
     */
    BaseClient.prototype._process = function (promise) {
        var _this = this;
        this._numProcessing += 1;
        void promise.then(function (value) {
            _this._numProcessing -= 1;
            return value;
        }, function (reason) {
            _this._numProcessing -= 1;
            return reason;
        });
    };
    /**
     * Verifies that return value of configured `beforeSend` is of expected type.
     */
    BaseClient.prototype._ensureBeforeSendRv = function (rv) {
        var nullErr = '`beforeSend` method has to return `null` or a valid event.';
        if (isThenable(rv)) {
            return rv.then(function (event) {
                if (!(isPlainObject(event) || event === null)) {
                    throw new SentryError(nullErr);
                }
                return event;
            }, function (e) {
                throw new SentryError("beforeSend rejected with " + e);
            });
        }
        else if (!(isPlainObject(rv) || rv === null)) {
            throw new SentryError(nullErr);
        }
        return rv;
    };
    return BaseClient;
}());

/** Noop transport */
var NoopTransport = /** @class */ (function () {
    function NoopTransport() {
    }
    /**
     * @inheritDoc
     */
    NoopTransport.prototype.sendEvent = function (_) {
        return SyncPromise.resolve({
            reason: "NoopTransport: Event has been skipped because no Dsn is configured.",
            status: Status.Skipped,
        });
    };
    /**
     * @inheritDoc
     */
    NoopTransport.prototype.close = function (_) {
        return SyncPromise.resolve(true);
    };
    return NoopTransport;
}());

/**
 * This is the base implemention of a Backend.
 * @hidden
 */
var BaseBackend = /** @class */ (function () {
    /** Creates a new backend instance. */
    function BaseBackend(options) {
        this._options = options;
        if (!this._options.dsn) {
            logger.warn('No DSN provided, backend will not do anything.');
        }
        this._transport = this._setupTransport();
    }
    /**
     * @inheritDoc
     */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/explicit-module-boundary-types
    BaseBackend.prototype.eventFromException = function (_exception, _hint) {
        throw new SentryError('Backend has to implement `eventFromException` method');
    };
    /**
     * @inheritDoc
     */
    BaseBackend.prototype.eventFromMessage = function (_message, _level, _hint) {
        throw new SentryError('Backend has to implement `eventFromMessage` method');
    };
    /**
     * @inheritDoc
     */
    BaseBackend.prototype.sendEvent = function (event) {
        void this._transport.sendEvent(event).then(null, function (reason) {
            logger.error("Error while sending event: " + reason);
        });
    };
    /**
     * @inheritDoc
     */
    BaseBackend.prototype.sendSession = function (session) {
        if (!this._transport.sendSession) {
            logger.warn("Dropping session because custom transport doesn't implement sendSession");
            return;
        }
        void this._transport.sendSession(session).then(null, function (reason) {
            logger.error("Error while sending session: " + reason);
        });
    };
    /**
     * @inheritDoc
     */
    BaseBackend.prototype.getTransport = function () {
        return this._transport;
    };
    /**
     * Sets up the transport so it can be used later to send requests.
     */
    BaseBackend.prototype._setupTransport = function () {
        return new NoopTransport();
    };
    return BaseBackend;
}());

/** Extract sdk info from from the API metadata */
function getSdkMetadataForEnvelopeHeader(api) {
    if (!api.metadata || !api.metadata.sdk) {
        return;
    }
    var _a = api.metadata.sdk, name = _a.name, version = _a.version;
    return { name: name, version: version };
}
/**
 * Apply SdkInfo (name, version, packages, integrations) to the corresponding event key.
 * Merge with existing data if any.
 **/
function enhanceEventWithSdkInfo(event, sdkInfo) {
    if (!sdkInfo) {
        return event;
    }
    event.sdk = event.sdk || {};
    event.sdk.name = event.sdk.name || sdkInfo.name;
    event.sdk.version = event.sdk.version || sdkInfo.version;
    event.sdk.integrations = __spread$1((event.sdk.integrations || []), (sdkInfo.integrations || []));
    event.sdk.packages = __spread$1((event.sdk.packages || []), (sdkInfo.packages || []));
    return event;
}
/** Creates a SentryRequest from a Session. */
function sessionToSentryRequest(session, api) {
    var sdkInfo = getSdkMetadataForEnvelopeHeader(api);
    var envelopeHeaders = JSON.stringify(__assign$1(__assign$1({ sent_at: new Date().toISOString() }, (sdkInfo && { sdk: sdkInfo })), (api.forceEnvelope() && { dsn: api.getDsn().toString() })));
    // I know this is hacky but we don't want to add `session` to request type since it's never rate limited
    var type = 'aggregates' in session ? 'sessions' : 'session';
    var itemHeaders = JSON.stringify({
        type: type,
    });
    return {
        body: envelopeHeaders + "\n" + itemHeaders + "\n" + JSON.stringify(session),
        type: type,
        url: api.getEnvelopeEndpointWithUrlEncodedAuth(),
    };
}
/** Creates a SentryRequest from an event. */
function eventToSentryRequest(event, api) {
    var sdkInfo = getSdkMetadataForEnvelopeHeader(api);
    var eventType = event.type || 'event';
    var useEnvelope = eventType === 'transaction' || api.forceEnvelope();
    var _a = event.debug_meta || {}, transactionSampling = _a.transactionSampling, metadata = __rest(_a, ["transactionSampling"]);
    var _b = transactionSampling || {}, samplingMethod = _b.method, sampleRate = _b.rate;
    if (Object.keys(metadata).length === 0) {
        delete event.debug_meta;
    }
    else {
        event.debug_meta = metadata;
    }
    var req = {
        body: JSON.stringify(sdkInfo ? enhanceEventWithSdkInfo(event, api.metadata.sdk) : event),
        type: eventType,
        url: useEnvelope ? api.getEnvelopeEndpointWithUrlEncodedAuth() : api.getStoreEndpointWithUrlEncodedAuth(),
    };
    // https://develop.sentry.dev/sdk/envelopes/
    // Since we don't need to manipulate envelopes nor store them, there is no
    // exported concept of an Envelope with operations including serialization and
    // deserialization. Instead, we only implement a minimal subset of the spec to
    // serialize events inline here.
    if (useEnvelope) {
        var envelopeHeaders = JSON.stringify(__assign$1(__assign$1({ event_id: event.event_id, sent_at: new Date().toISOString() }, (sdkInfo && { sdk: sdkInfo })), (api.forceEnvelope() && { dsn: api.getDsn().toString() })));
        var itemHeaders = JSON.stringify({
            type: eventType,
            // TODO: Right now, sampleRate may or may not be defined (it won't be in the cases of inheritance and
            // explicitly-set sampling decisions). Are we good with that?
            sample_rates: [{ id: samplingMethod, rate: sampleRate }],
        });
        // The trailing newline is optional. We intentionally don't send it to avoid
        // sending unnecessary bytes.
        //
        // const envelope = `${envelopeHeaders}\n${itemHeaders}\n${req.body}\n`;
        var envelope = envelopeHeaders + "\n" + itemHeaders + "\n" + req.body;
        req.body = envelope;
    }
    return req;
}

/**
 * Internal function to create a new SDK client instance. The client is
 * installed and then bound to the current scope.
 *
 * @param clientClass The client class to instantiate.
 * @param options Options to pass to the client.
 */
function initAndBind(clientClass, options) {
    var _a;
    if (options.debug === true) {
        logger.enable();
    }
    var hub = getCurrentHub();
    (_a = hub.getScope()) === null || _a === void 0 ? void 0 : _a.update(options.initialScope);
    var client = new clientClass(options);
    hub.bindClient(client);
}

var SDK_VERSION = '6.16.1';

var originalFunctionToString;
/** Patch toString calls to return proper name for wrapped functions */
var FunctionToString = /** @class */ (function () {
    function FunctionToString() {
        /**
         * @inheritDoc
         */
        this.name = FunctionToString.id;
    }
    /**
     * @inheritDoc
     */
    FunctionToString.prototype.setupOnce = function () {
        // eslint-disable-next-line @typescript-eslint/unbound-method
        originalFunctionToString = Function.prototype.toString;
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        Function.prototype.toString = function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var context = this.__sentry_original__ || this;
            return originalFunctionToString.apply(context, args);
        };
    };
    /**
     * @inheritDoc
     */
    FunctionToString.id = 'FunctionToString';
    return FunctionToString;
}());

// "Script error." is hard coded into browsers for errors that it can't read.
// this is the result of a script being pulled in from an external domain and CORS.
var DEFAULT_IGNORE_ERRORS = [/^Script error\.?$/, /^Javascript error: Script error\.? on line 0$/];
/** Inbound filters configurable by the user */
var InboundFilters = /** @class */ (function () {
    function InboundFilters(_options) {
        if (_options === void 0) { _options = {}; }
        this._options = _options;
        /**
         * @inheritDoc
         */
        this.name = InboundFilters.id;
    }
    /**
     * @inheritDoc
     */
    InboundFilters.prototype.setupOnce = function () {
        addGlobalEventProcessor(function (event) {
            var hub = getCurrentHub();
            if (!hub) {
                return event;
            }
            var self = hub.getIntegration(InboundFilters);
            if (self) {
                var client = hub.getClient();
                var clientOptions = client ? client.getOptions() : {};
                // This checks prevents most of the occurrences of the bug linked below:
                // https://github.com/getsentry/sentry-javascript/issues/2622
                // The bug is caused by multiple SDK instances, where one is minified and one is using non-mangled code.
                // Unfortunatelly we cannot fix it reliably (thus reserved property in rollup's terser config),
                // as we cannot force people using multiple instances in their apps to sync SDK versions.
                var options = typeof self._mergeOptions === 'function' ? self._mergeOptions(clientOptions) : {};
                if (typeof self._shouldDropEvent !== 'function') {
                    return event;
                }
                return self._shouldDropEvent(event, options) ? null : event;
            }
            return event;
        });
    };
    /** JSDoc */
    InboundFilters.prototype._shouldDropEvent = function (event, options) {
        if (this._isSentryError(event, options)) {
            logger.warn("Event dropped due to being internal Sentry Error.\nEvent: " + getEventDescription(event));
            return true;
        }
        if (this._isIgnoredError(event, options)) {
            logger.warn("Event dropped due to being matched by `ignoreErrors` option.\nEvent: " + getEventDescription(event));
            return true;
        }
        if (this._isDeniedUrl(event, options)) {
            logger.warn("Event dropped due to being matched by `denyUrls` option.\nEvent: " + getEventDescription(event) + ".\nUrl: " + this._getEventFilterUrl(event));
            return true;
        }
        if (!this._isAllowedUrl(event, options)) {
            logger.warn("Event dropped due to not being matched by `allowUrls` option.\nEvent: " + getEventDescription(event) + ".\nUrl: " + this._getEventFilterUrl(event));
            return true;
        }
        return false;
    };
    /** JSDoc */
    InboundFilters.prototype._isSentryError = function (event, options) {
        if (!options.ignoreInternal) {
            return false;
        }
        try {
            return ((event &&
                event.exception &&
                event.exception.values &&
                event.exception.values[0] &&
                event.exception.values[0].type === 'SentryError') ||
                false);
        }
        catch (_oO) {
            return false;
        }
    };
    /** JSDoc */
    InboundFilters.prototype._isIgnoredError = function (event, options) {
        if (!options.ignoreErrors || !options.ignoreErrors.length) {
            return false;
        }
        return this._getPossibleEventMessages(event).some(function (message) {
            // Not sure why TypeScript complains here...
            return options.ignoreErrors.some(function (pattern) { return isMatchingPattern(message, pattern); });
        });
    };
    /** JSDoc */
    InboundFilters.prototype._isDeniedUrl = function (event, options) {
        // TODO: Use Glob instead?
        if (!options.denyUrls || !options.denyUrls.length) {
            return false;
        }
        var url = this._getEventFilterUrl(event);
        return !url ? false : options.denyUrls.some(function (pattern) { return isMatchingPattern(url, pattern); });
    };
    /** JSDoc */
    InboundFilters.prototype._isAllowedUrl = function (event, options) {
        // TODO: Use Glob instead?
        if (!options.allowUrls || !options.allowUrls.length) {
            return true;
        }
        var url = this._getEventFilterUrl(event);
        return !url ? true : options.allowUrls.some(function (pattern) { return isMatchingPattern(url, pattern); });
    };
    /** JSDoc */
    InboundFilters.prototype._mergeOptions = function (clientOptions) {
        if (clientOptions === void 0) { clientOptions = {}; }
        return {
            allowUrls: __spread$1((this._options.whitelistUrls || []), (this._options.allowUrls || []), (clientOptions.whitelistUrls || []), (clientOptions.allowUrls || [])),
            denyUrls: __spread$1((this._options.blacklistUrls || []), (this._options.denyUrls || []), (clientOptions.blacklistUrls || []), (clientOptions.denyUrls || [])),
            ignoreErrors: __spread$1((this._options.ignoreErrors || []), (clientOptions.ignoreErrors || []), DEFAULT_IGNORE_ERRORS),
            ignoreInternal: typeof this._options.ignoreInternal !== 'undefined' ? this._options.ignoreInternal : true,
        };
    };
    /** JSDoc */
    InboundFilters.prototype._getPossibleEventMessages = function (event) {
        if (event.message) {
            return [event.message];
        }
        if (event.exception) {
            try {
                var _a = (event.exception.values && event.exception.values[0]) || {}, _b = _a.type, type = _b === void 0 ? '' : _b, _c = _a.value, value = _c === void 0 ? '' : _c;
                return ["" + value, type + ": " + value];
            }
            catch (oO) {
                logger.error("Cannot extract message for event " + getEventDescription(event));
                return [];
            }
        }
        return [];
    };
    /** JSDoc */
    InboundFilters.prototype._getLastValidUrl = function (frames) {
        if (frames === void 0) { frames = []; }
        var _a, _b;
        for (var i = frames.length - 1; i >= 0; i--) {
            var frame = frames[i];
            if (((_a = frame) === null || _a === void 0 ? void 0 : _a.filename) !== '<anonymous>' && ((_b = frame) === null || _b === void 0 ? void 0 : _b.filename) !== '[native code]') {
                return frame.filename || null;
            }
        }
        return null;
    };
    /** JSDoc */
    InboundFilters.prototype._getEventFilterUrl = function (event) {
        try {
            if (event.stacktrace) {
                var frames_1 = event.stacktrace.frames;
                return this._getLastValidUrl(frames_1);
            }
            if (event.exception) {
                var frames_2 = event.exception.values && event.exception.values[0].stacktrace && event.exception.values[0].stacktrace.frames;
                return this._getLastValidUrl(frames_2);
            }
            return null;
        }
        catch (oO) {
            logger.error("Cannot extract url for event " + getEventDescription(event));
            return null;
        }
    };
    /**
     * @inheritDoc
     */
    InboundFilters.id = 'InboundFilters';
    return InboundFilters;
}());

/**
 * This was originally forked from https://github.com/occ/TraceKit, but has since been
 * largely modified and is now maintained as part of Sentry JS SDK.
 */
// global reference to slice
var UNKNOWN_FUNCTION = '?';
// Chromium based browsers: Chrome, Brave, new Opera, new Edge
var chrome$1 = /^\s*at (?:(.*?) ?\()?((?:file|https?|blob|chrome-extension|address|native|eval|webpack|<anonymous>|[-a-z]+:|.*bundle|\/).*?)(?::(\d+))?(?::(\d+))?\)?\s*$/i;
// gecko regex: `(?:bundle|\d+\.js)`: `bundle` is for react native, `\d+\.js` also but specifically for ram bundles because it
// generates filenames without a prefix like `file://` the filenames in the stacktrace are just 42.js
// We need this specific case for now because we want no other regex to match.
var gecko = /^\s*(.*?)(?:\((.*?)\))?(?:^|@)?((?:file|https?|blob|chrome|webpack|resource|moz-extension|capacitor).*?:\/.*?|\[native code\]|[^@]*(?:bundle|\d+\.js)|\/[\w\-. /=]+)(?::(\d+))?(?::(\d+))?\s*$/i;
var winjs = /^\s*at (?:((?:\[object object\])?.+) )?\(?((?:file|ms-appx|https?|webpack|blob):.*?):(\d+)(?::(\d+))?\)?\s*$/i;
var geckoEval = /(\S+) line (\d+)(?: > eval line \d+)* > eval/i;
var chromeEval = /\((\S*)(?::(\d+))(?::(\d+))\)/;
// Based on our own mapping pattern - https://github.com/getsentry/sentry/blob/9f08305e09866c8bd6d0c24f5b0aabdd7dd6c59c/src/sentry/lang/javascript/errormapping.py#L83-L108
var reactMinifiedRegexp = /Minified React error #\d+;/i;
/** JSDoc */
// eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/explicit-module-boundary-types
function computeStackTrace(ex) {
    var stack = null;
    var popSize = 0;
    if (ex) {
        if (typeof ex.framesToPop === 'number') {
            popSize = ex.framesToPop;
        }
        else if (reactMinifiedRegexp.test(ex.message)) {
            popSize = 1;
        }
    }
    try {
        // This must be tried first because Opera 10 *destroys*
        // its stacktrace property if you try to access the stack
        // property first!!
        stack = computeStackTraceFromStacktraceProp(ex);
        if (stack) {
            return popFrames(stack, popSize);
        }
    }
    catch (e) {
        // no-empty
    }
    try {
        stack = computeStackTraceFromStackProp(ex);
        if (stack) {
            return popFrames(stack, popSize);
        }
    }
    catch (e) {
        // no-empty
    }
    return {
        message: extractMessage(ex),
        name: ex && ex.name,
        stack: [],
        failed: true,
    };
}
/** JSDoc */
// eslint-disable-next-line @typescript-eslint/no-explicit-any, complexity
function computeStackTraceFromStackProp(ex) {
    var _a, _b;
    if (!ex || !ex.stack) {
        return null;
    }
    var stack = [];
    var lines = ex.stack.split('\n');
    var isEval;
    var submatch;
    var parts;
    var element;
    for (var i = 0; i < lines.length; ++i) {
        if ((parts = chrome$1.exec(lines[i]))) {
            var isNative = parts[2] && parts[2].indexOf('native') === 0; // start of line
            isEval = parts[2] && parts[2].indexOf('eval') === 0; // start of line
            if (isEval && (submatch = chromeEval.exec(parts[2]))) {
                // throw out eval line/column and use top-most line/column number
                parts[2] = submatch[1]; // url
                parts[3] = submatch[2]; // line
                parts[4] = submatch[3]; // column
            }
            // Arpad: Working with the regexp above is super painful. it is quite a hack, but just stripping the `address at `
            // prefix here seems like the quickest solution for now.
            var url = parts[2] && parts[2].indexOf('address at ') === 0 ? parts[2].substr('address at '.length) : parts[2];
            // Kamil: One more hack won't hurt us right? Understanding and adding more rules on top of these regexps right now
            // would be way too time consuming. (TODO: Rewrite whole RegExp to be more readable)
            var func = parts[1] || UNKNOWN_FUNCTION;
            _a = __read$2(extractSafariExtensionDetails(func, url), 2), func = _a[0], url = _a[1];
            element = {
                url: url,
                func: func,
                args: isNative ? [parts[2]] : [],
                line: parts[3] ? +parts[3] : null,
                column: parts[4] ? +parts[4] : null,
            };
        }
        else if ((parts = winjs.exec(lines[i]))) {
            element = {
                url: parts[2],
                func: parts[1] || UNKNOWN_FUNCTION,
                args: [],
                line: +parts[3],
                column: parts[4] ? +parts[4] : null,
            };
        }
        else if ((parts = gecko.exec(lines[i]))) {
            isEval = parts[3] && parts[3].indexOf(' > eval') > -1;
            if (isEval && (submatch = geckoEval.exec(parts[3]))) {
                // throw out eval line/column and use top-most line number
                parts[1] = parts[1] || "eval";
                parts[3] = submatch[1];
                parts[4] = submatch[2];
                parts[5] = ''; // no column when eval
            }
            else if (i === 0 && !parts[5] && ex.columnNumber !== void 0) {
                // FireFox uses this awesome columnNumber property for its top frame
                // Also note, Firefox's column number is 0-based and everything else expects 1-based,
                // so adding 1
                // NOTE: this hack doesn't work if top-most frame is eval
                stack[0].column = ex.columnNumber + 1;
            }
            var url = parts[3];
            var func = parts[1] || UNKNOWN_FUNCTION;
            _b = __read$2(extractSafariExtensionDetails(func, url), 2), func = _b[0], url = _b[1];
            element = {
                url: url,
                func: func,
                args: parts[2] ? parts[2].split(',') : [],
                line: parts[4] ? +parts[4] : null,
                column: parts[5] ? +parts[5] : null,
            };
        }
        else {
            continue;
        }
        if (!element.func && element.line) {
            element.func = UNKNOWN_FUNCTION;
        }
        stack.push(element);
    }
    if (!stack.length) {
        return null;
    }
    return {
        message: extractMessage(ex),
        name: ex.name,
        stack: stack,
    };
}
/** JSDoc */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function computeStackTraceFromStacktraceProp(ex) {
    if (!ex || !ex.stacktrace) {
        return null;
    }
    // Access and store the stacktrace property before doing ANYTHING
    // else to it because Opera is not very good at providing it
    // reliably in other circumstances.
    var stacktrace = ex.stacktrace;
    var opera10Regex = / line (\d+).*script (?:in )?(\S+)(?:: in function (\S+))?$/i;
    var opera11Regex = / line (\d+), column (\d+)\s*(?:in (?:<anonymous function: ([^>]+)>|([^)]+))\((.*)\))? in (.*):\s*$/i;
    var lines = stacktrace.split('\n');
    var stack = [];
    var parts;
    for (var line = 0; line < lines.length; line += 2) {
        var element = null;
        if ((parts = opera10Regex.exec(lines[line]))) {
            element = {
                url: parts[2],
                func: parts[3],
                args: [],
                line: +parts[1],
                column: null,
            };
        }
        else if ((parts = opera11Regex.exec(lines[line]))) {
            element = {
                url: parts[6],
                func: parts[3] || parts[4],
                args: parts[5] ? parts[5].split(',') : [],
                line: +parts[1],
                column: +parts[2],
            };
        }
        if (element) {
            if (!element.func && element.line) {
                element.func = UNKNOWN_FUNCTION;
            }
            stack.push(element);
        }
    }
    if (!stack.length) {
        return null;
    }
    return {
        message: extractMessage(ex),
        name: ex.name,
        stack: stack,
    };
}
/**
 * Safari web extensions, starting version unknown, can produce "frames-only" stacktraces.
 * What it means, is that instead of format like:
 *
 * Error: wat
 *   at function@url:row:col
 *   at function@url:row:col
 *   at function@url:row:col
 *
 * it produces something like:
 *
 *   function@url:row:col
 *   function@url:row:col
 *   function@url:row:col
 *
 * Because of that, it won't be captured by `chrome` RegExp and will fall into `Gecko` branch.
 * This function is extracted so that we can use it in both places without duplicating the logic.
 * Unfortunatelly "just" changing RegExp is too complicated now and making it pass all tests
 * and fix this case seems like an impossible, or at least way too time-consuming task.
 */
var extractSafariExtensionDetails = function (func, url) {
    var isSafariExtension = func.indexOf('safari-extension') !== -1;
    var isSafariWebExtension = func.indexOf('safari-web-extension') !== -1;
    return isSafariExtension || isSafariWebExtension
        ? [
            func.indexOf('@') !== -1 ? func.split('@')[0] : UNKNOWN_FUNCTION,
            isSafariExtension ? "safari-extension:" + url : "safari-web-extension:" + url,
        ]
        : [func, url];
};
/** Remove N number of frames from the stack */
function popFrames(stacktrace, popSize) {
    try {
        return __assign$2(__assign$2({}, stacktrace), { stack: stacktrace.stack.slice(popSize) });
    }
    catch (e) {
        return stacktrace;
    }
}
/**
 * There are cases where stacktrace.message is an Event object
 * https://github.com/getsentry/sentry-javascript/issues/1949
 * In this specific case we try to extract stacktrace.message.error.message
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function extractMessage(ex) {
    var message = ex && ex.message;
    if (!message) {
        return 'No error message';
    }
    if (message.error && typeof message.error.message === 'string') {
        return message.error.message;
    }
    return message;
}

var STACKTRACE_LIMIT = 50;
/**
 * This function creates an exception from an TraceKitStackTrace
 * @param stacktrace TraceKitStackTrace that will be converted to an exception
 * @hidden
 */
function exceptionFromStacktrace(stacktrace) {
    var frames = prepareFramesForEvent(stacktrace.stack);
    var exception = {
        type: stacktrace.name,
        value: stacktrace.message,
    };
    if (frames && frames.length) {
        exception.stacktrace = { frames: frames };
    }
    if (exception.type === undefined && exception.value === '') {
        exception.value = 'Unrecoverable error caught';
    }
    return exception;
}
/**
 * @hidden
 */
function eventFromPlainObject(exception, syntheticException, rejection) {
    var event = {
        exception: {
            values: [
                {
                    type: isEvent(exception) ? exception.constructor.name : rejection ? 'UnhandledRejection' : 'Error',
                    value: "Non-Error " + (rejection ? 'promise rejection' : 'exception') + " captured with keys: " + extractExceptionKeysForMessage(exception),
                },
            ],
        },
        extra: {
            __serialized__: normalizeToSize(exception),
        },
    };
    if (syntheticException) {
        var stacktrace = computeStackTrace(syntheticException);
        var frames_1 = prepareFramesForEvent(stacktrace.stack);
        event.stacktrace = {
            frames: frames_1,
        };
    }
    return event;
}
/**
 * @hidden
 */
function eventFromStacktrace(stacktrace) {
    var exception = exceptionFromStacktrace(stacktrace);
    return {
        exception: {
            values: [exception],
        },
    };
}
/**
 * @hidden
 */
function prepareFramesForEvent(stack) {
    if (!stack || !stack.length) {
        return [];
    }
    var localStack = stack;
    var firstFrameFunction = localStack[0].func || '';
    var lastFrameFunction = localStack[localStack.length - 1].func || '';
    // If stack starts with one of our API calls, remove it (starts, meaning it's the top of the stack - aka last call)
    if (firstFrameFunction.indexOf('captureMessage') !== -1 || firstFrameFunction.indexOf('captureException') !== -1) {
        localStack = localStack.slice(1);
    }
    // If stack ends with one of our internal API calls, remove it (ends, meaning it's the bottom of the stack - aka top-most call)
    if (lastFrameFunction.indexOf('sentryWrapped') !== -1) {
        localStack = localStack.slice(0, -1);
    }
    // The frame where the crash happened, should be the last entry in the array
    return localStack
        .slice(0, STACKTRACE_LIMIT)
        .map(function (frame) { return ({
        colno: frame.column === null ? undefined : frame.column,
        filename: frame.url || localStack[0].url,
        function: frame.func || '?',
        in_app: true,
        lineno: frame.line === null ? undefined : frame.line,
    }); })
        .reverse();
}

/**
 * Builds and Event from a Exception
 * @hidden
 */
function eventFromException(options, exception, hint) {
    var syntheticException = (hint && hint.syntheticException) || undefined;
    var event = eventFromUnknownInput(exception, syntheticException, {
        attachStacktrace: options.attachStacktrace,
    });
    addExceptionMechanism(event); // defaults to { type: 'generic', handled: true }
    event.level = Severity.Error;
    if (hint && hint.event_id) {
        event.event_id = hint.event_id;
    }
    return SyncPromise.resolve(event);
}
/**
 * Builds and Event from a Message
 * @hidden
 */
function eventFromMessage(options, message, level, hint) {
    if (level === void 0) { level = Severity.Info; }
    var syntheticException = (hint && hint.syntheticException) || undefined;
    var event = eventFromString(message, syntheticException, {
        attachStacktrace: options.attachStacktrace,
    });
    event.level = level;
    if (hint && hint.event_id) {
        event.event_id = hint.event_id;
    }
    return SyncPromise.resolve(event);
}
/**
 * @hidden
 */
function eventFromUnknownInput(exception, syntheticException, options) {
    if (options === void 0) { options = {}; }
    var event;
    if (isErrorEvent(exception) && exception.error) {
        // If it is an ErrorEvent with `error` property, extract it to get actual Error
        var errorEvent = exception;
        // eslint-disable-next-line no-param-reassign
        exception = errorEvent.error;
        event = eventFromStacktrace(computeStackTrace(exception));
        return event;
    }
    // If it is a `DOMError` (which is a legacy API, but still supported in some browsers) then we just extract the name
    // and message, as it doesn't provide anything else. According to the spec, all `DOMExceptions` should also be
    // `Error`s, but that's not the case in IE11, so in that case we treat it the same as we do a `DOMError`.
    //
    // https://developer.mozilla.org/en-US/docs/Web/API/DOMError
    // https://developer.mozilla.org/en-US/docs/Web/API/DOMException
    // https://webidl.spec.whatwg.org/#es-DOMException-specialness
    if (isDOMError(exception) || isDOMException(exception)) {
        var domException = exception;
        if ('stack' in exception) {
            event = eventFromStacktrace(computeStackTrace(exception));
        }
        else {
            var name_1 = domException.name || (isDOMError(domException) ? 'DOMError' : 'DOMException');
            var message = domException.message ? name_1 + ": " + domException.message : name_1;
            event = eventFromString(message, syntheticException, options);
            addExceptionTypeValue(event, message);
        }
        if ('code' in domException) {
            event.tags = __assign$2(__assign$2({}, event.tags), { 'DOMException.code': "" + domException.code });
        }
        return event;
    }
    if (isError(exception)) {
        // we have a real Error object, do nothing
        event = eventFromStacktrace(computeStackTrace(exception));
        return event;
    }
    if (isPlainObject(exception) || isEvent(exception)) {
        // If it is plain Object or Event, serialize it manually and extract options
        // This will allow us to group events based on top-level keys
        // which is much better than creating new group when any key/value change
        var objectException = exception;
        event = eventFromPlainObject(objectException, syntheticException, options.rejection);
        addExceptionMechanism(event, {
            synthetic: true,
        });
        return event;
    }
    // If none of previous checks were valid, then it means that it's not:
    // - an instance of DOMError
    // - an instance of DOMException
    // - an instance of Event
    // - an instance of Error
    // - a valid ErrorEvent (one with an error property)
    // - a plain Object
    //
    // So bail out and capture it as a simple message:
    event = eventFromString(exception, syntheticException, options);
    addExceptionTypeValue(event, "" + exception, undefined);
    addExceptionMechanism(event, {
        synthetic: true,
    });
    return event;
}
/**
 * @hidden
 */
function eventFromString(input, syntheticException, options) {
    if (options === void 0) { options = {}; }
    var event = {
        message: input,
    };
    if (options.attachStacktrace && syntheticException) {
        var stacktrace = computeStackTrace(syntheticException);
        var frames_1 = prepareFramesForEvent(stacktrace.stack);
        event.stacktrace = {
            frames: frames_1,
        };
    }
    return event;
}

var global$3 = getGlobalObject();
var cachedFetchImpl;
/**
 * A special usecase for incorrectly wrapped Fetch APIs in conjunction with ad-blockers.
 * Whenever someone wraps the Fetch API and returns the wrong promise chain,
 * this chain becomes orphaned and there is no possible way to capture it's rejections
 * other than allowing it bubble up to this very handler. eg.
 *
 * const f = window.fetch;
 * window.fetch = function () {
 *   const p = f.apply(this, arguments);
 *
 *   p.then(function() {
 *     console.log('hi.');
 *   });
 *
 *   return p;
 * }
 *
 * `p.then(function () { ... })` is producing a completely separate promise chain,
 * however, what's returned is `p` - the result of original `fetch` call.
 *
 * This mean, that whenever we use the Fetch API to send our own requests, _and_
 * some ad-blocker blocks it, this orphaned chain will _always_ reject,
 * effectively causing another event to be captured.
 * This makes a whole process become an infinite loop, which we need to somehow
 * deal with, and break it in one way or another.
 *
 * To deal with this issue, we are making sure that we _always_ use the real
 * browser Fetch API, instead of relying on what `window.fetch` exposes.
 * The only downside to this would be missing our own requests as breadcrumbs,
 * but because we are already not doing this, it should be just fine.
 *
 * Possible failed fetch error messages per-browser:
 *
 * Chrome:  Failed to fetch
 * Edge:    Failed to Fetch
 * Firefox: NetworkError when attempting to fetch resource
 * Safari:  resource blocked by content blocker
 */
function getNativeFetchImplementation() {
    var _a, _b;
    if (cachedFetchImpl) {
        return cachedFetchImpl;
    }
    /* eslint-disable @typescript-eslint/unbound-method */
    // Fast path to avoid DOM I/O
    if (isNativeFetch(global$3.fetch)) {
        return (cachedFetchImpl = global$3.fetch.bind(global$3));
    }
    var document = global$3.document;
    var fetchImpl = global$3.fetch;
    // eslint-disable-next-line deprecation/deprecation
    if (typeof ((_a = document) === null || _a === void 0 ? void 0 : _a.createElement) === "function") {
        try {
            var sandbox = document.createElement('iframe');
            sandbox.hidden = true;
            document.head.appendChild(sandbox);
            if ((_b = sandbox.contentWindow) === null || _b === void 0 ? void 0 : _b.fetch) {
                fetchImpl = sandbox.contentWindow.fetch;
            }
            document.head.removeChild(sandbox);
        }
        catch (e) {
            logger.warn('Could not create sandbox iframe for pure fetch check, bailing to window.fetch: ', e);
        }
    }
    return (cachedFetchImpl = fetchImpl.bind(global$3));
    /* eslint-enable @typescript-eslint/unbound-method */
}
/**
 * Sends sdk client report using sendBeacon or fetch as a fallback if available
 *
 * @param url report endpoint
 * @param body report payload
 */
function sendReport(url, body) {
    var isRealNavigator = Object.prototype.toString.call(global$3 && global$3.navigator) === '[object Navigator]';
    var hasSendBeacon = isRealNavigator && typeof global$3.navigator.sendBeacon === 'function';
    if (hasSendBeacon) {
        // Prevent illegal invocations - https://xgwang.me/posts/you-may-not-know-beacon/#it-may-throw-error%2C-be-sure-to-catch
        var sendBeacon = global$3.navigator.sendBeacon.bind(global$3.navigator);
        return sendBeacon(url, body);
    }
    if (supportsFetch()) {
        var fetch_1 = getNativeFetchImplementation();
        return forget(fetch_1(url, {
            body: body,
            method: 'POST',
            credentials: 'omit',
            keepalive: true,
        }));
    }
}

var CATEGORY_MAPPING = {
    event: 'error',
    transaction: 'transaction',
    session: 'session',
    attachment: 'attachment',
};
var global$2 = getGlobalObject();
/** Base Transport class implementation */
var BaseTransport = /** @class */ (function () {
    function BaseTransport(options) {
        var _this = this;
        this.options = options;
        /** A simple buffer holding all requests. */
        this._buffer = new PromiseBuffer(30);
        /** Locks transport after receiving rate limits in a response */
        this._rateLimits = {};
        this._outcomes = {};
        this._api = new API(options.dsn, options._metadata, options.tunnel);
        // eslint-disable-next-line deprecation/deprecation
        this.url = this._api.getStoreEndpointWithUrlEncodedAuth();
        if (this.options.sendClientReports && global$2.document) {
            global$2.document.addEventListener('visibilitychange', function () {
                if (global$2.document.visibilityState === 'hidden') {
                    _this._flushOutcomes();
                }
            });
        }
    }
    /**
     * @inheritDoc
     */
    BaseTransport.prototype.sendEvent = function (_) {
        throw new SentryError('Transport Class has to implement `sendEvent` method');
    };
    /**
     * @inheritDoc
     */
    BaseTransport.prototype.close = function (timeout) {
        return this._buffer.drain(timeout);
    };
    /**
     * @inheritDoc
     */
    BaseTransport.prototype.recordLostEvent = function (reason, category) {
        var _a;
        if (!this.options.sendClientReports) {
            return;
        }
        // We want to track each category (event, transaction, session) separately
        // but still keep the distinction between different type of outcomes.
        // We could use nested maps, but it's much easier to read and type this way.
        // A correct type for map-based implementation if we want to go that route
        // would be `Partial<Record<SentryRequestType, Partial<Record<Outcome, number>>>>`
        var key = CATEGORY_MAPPING[category] + ":" + reason;
        logger.log("Adding outcome: " + key);
        this._outcomes[key] = (_a = this._outcomes[key], (_a !== null && _a !== void 0 ? _a : 0)) + 1;
    };
    /**
     * Send outcomes as an envelope
     */
    BaseTransport.prototype._flushOutcomes = function () {
        if (!this.options.sendClientReports) {
            return;
        }
        var outcomes = this._outcomes;
        this._outcomes = {};
        // Nothing to send
        if (!Object.keys(outcomes).length) {
            logger.log('No outcomes to flush');
            return;
        }
        logger.log("Flushing outcomes:\n" + JSON.stringify(outcomes, null, 2));
        var url = this._api.getEnvelopeEndpointWithUrlEncodedAuth();
        // Envelope header is required to be at least an empty object
        var envelopeHeader = JSON.stringify(__assign$2({}, (this.options.tunnel && { dsn: this._api.getDsn().toString() })));
        var itemHeaders = JSON.stringify({
            type: 'client_report',
        });
        var item = JSON.stringify({
            timestamp: dateTimestampInSeconds(),
            discarded_events: Object.keys(outcomes).map(function (key) {
                var _a = __read$2(key.split(':'), 2), category = _a[0], reason = _a[1];
                return {
                    reason: reason,
                    category: category,
                    quantity: outcomes[key],
                };
            }),
        });
        var envelope = envelopeHeader + "\n" + itemHeaders + "\n" + item;
        try {
            sendReport(url, envelope);
        }
        catch (e) {
            logger.error(e);
        }
    };
    /**
     * Handle Sentry repsonse for promise-based transports.
     */
    BaseTransport.prototype._handleResponse = function (_a) {
        var requestType = _a.requestType, response = _a.response, headers = _a.headers, resolve = _a.resolve, reject = _a.reject;
        var status = Status.fromHttpCode(response.status);
        /**
         * "The name is case-insensitive."
         * https://developer.mozilla.org/en-US/docs/Web/API/Headers/get
         */
        var limited = this._handleRateLimit(headers);
        if (limited)
            logger.warn("Too many " + requestType + " requests, backing off until: " + this._disabledUntil(requestType));
        if (status === Status.Success) {
            resolve({ status: status });
            return;
        }
        reject(response);
    };
    /**
     * Gets the time that given category is disabled until for rate limiting
     */
    BaseTransport.prototype._disabledUntil = function (requestType) {
        var category = CATEGORY_MAPPING[requestType];
        return this._rateLimits[category] || this._rateLimits.all;
    };
    /**
     * Checks if a category is rate limited
     */
    BaseTransport.prototype._isRateLimited = function (requestType) {
        return this._disabledUntil(requestType) > new Date(Date.now());
    };
    /**
     * Sets internal _rateLimits from incoming headers. Returns true if headers contains a non-empty rate limiting header.
     */
    BaseTransport.prototype._handleRateLimit = function (headers) {
        var e_1, _a, e_2, _b;
        var now = Date.now();
        var rlHeader = headers['x-sentry-rate-limits'];
        var raHeader = headers['retry-after'];
        if (rlHeader) {
            try {
                // rate limit headers are of the form
                //     <header>,<header>,..
                // where each <header> is of the form
                //     <retry_after>: <categories>: <scope>: <reason_code>
                // where
                //     <retry_after> is a delay in ms
                //     <categories> is the event type(s) (error, transaction, etc) being rate limited and is of the form
                //         <category>;<category>;...
                //     <scope> is what's being limited (org, project, or key) - ignored by SDK
                //     <reason_code> is an arbitrary string like "org_quota" - ignored by SDK
                for (var _c = __values$1(rlHeader.trim().split(',')), _d = _c.next(); !_d.done; _d = _c.next()) {
                    var limit = _d.value;
                    var parameters = limit.split(':', 2);
                    var headerDelay = parseInt(parameters[0], 10);
                    var delay = (!isNaN(headerDelay) ? headerDelay : 60) * 1000; // 60sec default
                    try {
                        for (var _e = (e_2 = void 0, __values$1(parameters[1].split(';'))), _f = _e.next(); !_f.done; _f = _e.next()) {
                            var category = _f.value;
                            this._rateLimits[category || 'all'] = new Date(now + delay);
                        }
                    }
                    catch (e_2_1) { e_2 = { error: e_2_1 }; }
                    finally {
                        try {
                            if (_f && !_f.done && (_b = _e.return)) _b.call(_e);
                        }
                        finally { if (e_2) throw e_2.error; }
                    }
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
                }
                finally { if (e_1) throw e_1.error; }
            }
            return true;
        }
        else if (raHeader) {
            this._rateLimits.all = new Date(now + parseRetryAfterHeader(now, raHeader));
            return true;
        }
        return false;
    };
    return BaseTransport;
}());

/** `fetch` based transport */
var FetchTransport = /** @class */ (function (_super) {
    __extends$1(FetchTransport, _super);
    function FetchTransport(options, fetchImpl) {
        if (fetchImpl === void 0) { fetchImpl = getNativeFetchImplementation(); }
        var _this = _super.call(this, options) || this;
        _this._fetch = fetchImpl;
        return _this;
    }
    /**
     * @inheritDoc
     */
    FetchTransport.prototype.sendEvent = function (event) {
        return this._sendRequest(eventToSentryRequest(event, this._api), event);
    };
    /**
     * @inheritDoc
     */
    FetchTransport.prototype.sendSession = function (session) {
        return this._sendRequest(sessionToSentryRequest(session, this._api), session);
    };
    /**
     * @param sentryRequest Prepared SentryRequest to be delivered
     * @param originalPayload Original payload used to create SentryRequest
     */
    FetchTransport.prototype._sendRequest = function (sentryRequest, originalPayload) {
        var _this = this;
        if (this._isRateLimited(sentryRequest.type)) {
            this.recordLostEvent(Outcome.RateLimitBackoff, sentryRequest.type);
            return Promise.reject({
                event: originalPayload,
                type: sentryRequest.type,
                reason: "Transport for " + sentryRequest.type + " requests locked till " + this._disabledUntil(sentryRequest.type) + " due to too many requests.",
                status: 429,
            });
        }
        var options = {
            body: sentryRequest.body,
            method: 'POST',
            // Despite all stars in the sky saying that Edge supports old draft syntax, aka 'never', 'always', 'origin' and 'default
            // https://caniuse.com/#feat=referrer-policy
            // It doesn't. And it throw exception instead of ignoring this parameter...
            // REF: https://github.com/getsentry/raven-js/issues/1233
            referrerPolicy: (supportsReferrerPolicy() ? 'origin' : ''),
        };
        if (this.options.fetchParameters !== undefined) {
            Object.assign(options, this.options.fetchParameters);
        }
        if (this.options.headers !== undefined) {
            options.headers = this.options.headers;
        }
        return this._buffer
            .add(function () {
            return new SyncPromise(function (resolve, reject) {
                void _this._fetch(sentryRequest.url, options)
                    .then(function (response) {
                    var headers = {
                        'x-sentry-rate-limits': response.headers.get('X-Sentry-Rate-Limits'),
                        'retry-after': response.headers.get('Retry-After'),
                    };
                    _this._handleResponse({
                        requestType: sentryRequest.type,
                        response: response,
                        headers: headers,
                        resolve: resolve,
                        reject: reject,
                    });
                })
                    .catch(reject);
            });
        })
            .then(undefined, function (reason) {
            // It's either buffer rejection or any other xhr/fetch error, which are treated as NetworkError.
            if (reason instanceof SentryError) {
                _this.recordLostEvent(Outcome.QueueOverflow, sentryRequest.type);
            }
            else {
                _this.recordLostEvent(Outcome.NetworkError, sentryRequest.type);
            }
            throw reason;
        });
    };
    return FetchTransport;
}(BaseTransport));

/** `XHR` based transport */
var XHRTransport = /** @class */ (function (_super) {
    __extends$1(XHRTransport, _super);
    function XHRTransport() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    /**
     * @inheritDoc
     */
    XHRTransport.prototype.sendEvent = function (event) {
        return this._sendRequest(eventToSentryRequest(event, this._api), event);
    };
    /**
     * @inheritDoc
     */
    XHRTransport.prototype.sendSession = function (session) {
        return this._sendRequest(sessionToSentryRequest(session, this._api), session);
    };
    /**
     * @param sentryRequest Prepared SentryRequest to be delivered
     * @param originalPayload Original payload used to create SentryRequest
     */
    XHRTransport.prototype._sendRequest = function (sentryRequest, originalPayload) {
        var _this = this;
        if (this._isRateLimited(sentryRequest.type)) {
            this.recordLostEvent(Outcome.RateLimitBackoff, sentryRequest.type);
            return Promise.reject({
                event: originalPayload,
                type: sentryRequest.type,
                reason: "Transport for " + sentryRequest.type + " requests locked till " + this._disabledUntil(sentryRequest.type) + " due to too many requests.",
                status: 429,
            });
        }
        return this._buffer
            .add(function () {
            return new SyncPromise(function (resolve, reject) {
                var request = new XMLHttpRequest();
                request.onreadystatechange = function () {
                    if (request.readyState === 4) {
                        var headers = {
                            'x-sentry-rate-limits': request.getResponseHeader('X-Sentry-Rate-Limits'),
                            'retry-after': request.getResponseHeader('Retry-After'),
                        };
                        _this._handleResponse({ requestType: sentryRequest.type, response: request, headers: headers, resolve: resolve, reject: reject });
                    }
                };
                request.open('POST', sentryRequest.url);
                for (var header in _this.options.headers) {
                    if (Object.prototype.hasOwnProperty.call(_this.options.headers, header)) {
                        request.setRequestHeader(header, _this.options.headers[header]);
                    }
                }
                request.send(sentryRequest.body);
            });
        })
            .then(undefined, function (reason) {
            // It's either buffer rejection or any other xhr/fetch error, which are treated as NetworkError.
            if (reason instanceof SentryError) {
                _this.recordLostEvent(Outcome.QueueOverflow, sentryRequest.type);
            }
            else {
                _this.recordLostEvent(Outcome.NetworkError, sentryRequest.type);
            }
            throw reason;
        });
    };
    return XHRTransport;
}(BaseTransport));

/**
 * The Sentry Browser SDK Backend.
 * @hidden
 */
var BrowserBackend = /** @class */ (function (_super) {
    __extends$1(BrowserBackend, _super);
    function BrowserBackend() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    /**
     * @inheritDoc
     */
    BrowserBackend.prototype.eventFromException = function (exception, hint) {
        return eventFromException(this._options, exception, hint);
    };
    /**
     * @inheritDoc
     */
    BrowserBackend.prototype.eventFromMessage = function (message, level, hint) {
        if (level === void 0) { level = Severity.Info; }
        return eventFromMessage(this._options, message, level, hint);
    };
    /**
     * @inheritDoc
     */
    BrowserBackend.prototype._setupTransport = function () {
        if (!this._options.dsn) {
            // We return the noop transport here in case there is no Dsn.
            return _super.prototype._setupTransport.call(this);
        }
        var transportOptions = __assign$2(__assign$2({}, this._options.transportOptions), { dsn: this._options.dsn, tunnel: this._options.tunnel, sendClientReports: this._options.sendClientReports, _metadata: this._options._metadata });
        if (this._options.transport) {
            return new this._options.transport(transportOptions);
        }
        if (supportsFetch()) {
            return new FetchTransport(transportOptions);
        }
        return new XHRTransport(transportOptions);
    };
    return BrowserBackend;
}(BaseBackend));

var global$1 = getGlobalObject();
var ignoreOnError = 0;
/**
 * @hidden
 */
function shouldIgnoreOnError() {
    return ignoreOnError > 0;
}
/**
 * @hidden
 */
function ignoreNextOnError() {
    // onerror should trigger before setTimeout
    ignoreOnError += 1;
    setTimeout(function () {
        ignoreOnError -= 1;
    });
}
/**
 * Instruments the given function and sends an event to Sentry every time the
 * function throws an exception.
 *
 * @param fn A function to wrap.
 * @returns The wrapped function.
 * @hidden
 */
function wrap(fn, options, before) {
    if (options === void 0) { options = {}; }
    if (typeof fn !== 'function') {
        return fn;
    }
    try {
        // We don't wanna wrap it twice
        if (fn.__sentry__) {
            return fn;
        }
        // If this has already been wrapped in the past, return that wrapped function
        if (fn.__sentry_wrapped__) {
            return fn.__sentry_wrapped__;
        }
    }
    catch (e) {
        // Just accessing custom props in some Selenium environments
        // can cause a "Permission denied" exception (see raven-js#495).
        // Bail on wrapping and return the function as-is (defers to window.onerror).
        return fn;
    }
    /* eslint-disable prefer-rest-params */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    var sentryWrapped = function () {
        var args = Array.prototype.slice.call(arguments);
        try {
            if (before && typeof before === 'function') {
                before.apply(this, arguments);
            }
            // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/no-unsafe-member-access
            var wrappedArguments = args.map(function (arg) { return wrap(arg, options); });
            if (fn.handleEvent) {
                // Attempt to invoke user-land function
                // NOTE: If you are a Sentry user, and you are seeing this stack frame, it
                //       means the sentry.javascript SDK caught an error invoking your application code. This
                //       is expected behavior and NOT indicative of a bug with sentry.javascript.
                // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
                return fn.handleEvent.apply(this, wrappedArguments);
            }
            // Attempt to invoke user-land function
            // NOTE: If you are a Sentry user, and you are seeing this stack frame, it
            //       means the sentry.javascript SDK caught an error invoking your application code. This
            //       is expected behavior and NOT indicative of a bug with sentry.javascript.
            return fn.apply(this, wrappedArguments);
        }
        catch (ex) {
            ignoreNextOnError();
            withScope(function (scope) {
                scope.addEventProcessor(function (event) {
                    var processedEvent = __assign$2({}, event);
                    if (options.mechanism) {
                        addExceptionTypeValue(processedEvent, undefined, undefined);
                        addExceptionMechanism(processedEvent, options.mechanism);
                    }
                    processedEvent.extra = __assign$2(__assign$2({}, processedEvent.extra), { arguments: args });
                    return processedEvent;
                });
                captureException(ex);
            });
            throw ex;
        }
    };
    /* eslint-enable prefer-rest-params */
    // Accessing some objects may throw
    // ref: https://github.com/getsentry/sentry-javascript/issues/1168
    try {
        for (var property in fn) {
            if (Object.prototype.hasOwnProperty.call(fn, property)) {
                sentryWrapped[property] = fn[property];
            }
        }
    }
    catch (_oO) { } // eslint-disable-line no-empty
    fn.prototype = fn.prototype || {};
    sentryWrapped.prototype = fn.prototype;
    Object.defineProperty(fn, '__sentry_wrapped__', {
        enumerable: false,
        value: sentryWrapped,
    });
    // Signal that this function has been wrapped/filled already
    // for both debugging and to prevent it to being wrapped/filled twice
    Object.defineProperties(sentryWrapped, {
        __sentry__: {
            enumerable: false,
            value: true,
        },
        __sentry_original__: {
            enumerable: false,
            value: fn,
        },
    });
    // Restore original function name (not all browsers allow that)
    try {
        var descriptor = Object.getOwnPropertyDescriptor(sentryWrapped, 'name');
        if (descriptor.configurable) {
            Object.defineProperty(sentryWrapped, 'name', {
                get: function () {
                    return fn.name;
                },
            });
        }
        // eslint-disable-next-line no-empty
    }
    catch (_oO) { }
    return sentryWrapped;
}
/**
 * Injects the Report Dialog script
 * @hidden
 */
function injectReportDialog(options) {
    if (options === void 0) { options = {}; }
    if (!global$1.document) {
        return;
    }
    if (!options.eventId) {
        logger.error("Missing eventId option in showReportDialog call");
        return;
    }
    if (!options.dsn) {
        logger.error("Missing dsn option in showReportDialog call");
        return;
    }
    var script = global$1.document.createElement('script');
    script.async = true;
    script.src = new API(options.dsn).getReportDialogEndpoint(options);
    if (options.onLoad) {
        // eslint-disable-next-line @typescript-eslint/unbound-method
        script.onload = options.onLoad;
    }
    var injectionPoint = global$1.document.head || global$1.document.body;
    if (injectionPoint) {
        injectionPoint.appendChild(script);
    }
}

/** Global handlers */
var GlobalHandlers = /** @class */ (function () {
    /** JSDoc */
    function GlobalHandlers(options) {
        /**
         * @inheritDoc
         */
        this.name = GlobalHandlers.id;
        /** JSDoc */
        this._onErrorHandlerInstalled = false;
        /** JSDoc */
        this._onUnhandledRejectionHandlerInstalled = false;
        this._options = __assign$2({ onerror: true, onunhandledrejection: true }, options);
    }
    /**
     * @inheritDoc
     */
    GlobalHandlers.prototype.setupOnce = function () {
        Error.stackTraceLimit = 50;
        if (this._options.onerror) {
            logger.log('Global Handler attached: onerror');
            this._installGlobalOnErrorHandler();
        }
        if (this._options.onunhandledrejection) {
            logger.log('Global Handler attached: onunhandledrejection');
            this._installGlobalOnUnhandledRejectionHandler();
        }
    };
    /** JSDoc */
    GlobalHandlers.prototype._installGlobalOnErrorHandler = function () {
        var _this = this;
        if (this._onErrorHandlerInstalled) {
            return;
        }
        addInstrumentationHandler({
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            callback: function (data) {
                var error = data.error;
                var currentHub = getCurrentHub();
                var hasIntegration = currentHub.getIntegration(GlobalHandlers);
                var isFailedOwnDelivery = error && error.__sentry_own_request__ === true;
                if (!hasIntegration || shouldIgnoreOnError() || isFailedOwnDelivery) {
                    return;
                }
                var client = currentHub.getClient();
                var event = error === undefined && isString(data.msg)
                    ? _this._eventFromIncompleteOnError(data.msg, data.url, data.line, data.column)
                    : _this._enhanceEventWithInitialFrame(eventFromUnknownInput(error || data.msg, undefined, {
                        attachStacktrace: client && client.getOptions().attachStacktrace,
                        rejection: false,
                    }), data.url, data.line, data.column);
                addExceptionMechanism(event, {
                    handled: false,
                    type: 'onerror',
                });
                currentHub.captureEvent(event, {
                    originalException: error,
                });
            },
            type: 'error',
        });
        this._onErrorHandlerInstalled = true;
    };
    /** JSDoc */
    GlobalHandlers.prototype._installGlobalOnUnhandledRejectionHandler = function () {
        var _this = this;
        if (this._onUnhandledRejectionHandlerInstalled) {
            return;
        }
        addInstrumentationHandler({
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            callback: function (e) {
                var error = e;
                // dig the object of the rejection out of known event types
                try {
                    // PromiseRejectionEvents store the object of the rejection under 'reason'
                    // see https://developer.mozilla.org/en-US/docs/Web/API/PromiseRejectionEvent
                    if ('reason' in e) {
                        error = e.reason;
                    }
                    // something, somewhere, (likely a browser extension) effectively casts PromiseRejectionEvents
                    // to CustomEvents, moving the `promise` and `reason` attributes of the PRE into
                    // the CustomEvent's `detail` attribute, since they're not part of CustomEvent's spec
                    // see https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent and
                    // https://github.com/getsentry/sentry-javascript/issues/2380
                    else if ('detail' in e && 'reason' in e.detail) {
                        error = e.detail.reason;
                    }
                }
                catch (_oO) {
                    // no-empty
                }
                var currentHub = getCurrentHub();
                var hasIntegration = currentHub.getIntegration(GlobalHandlers);
                var isFailedOwnDelivery = error && error.__sentry_own_request__ === true;
                if (!hasIntegration || shouldIgnoreOnError() || isFailedOwnDelivery) {
                    return true;
                }
                var client = currentHub.getClient();
                var event = isPrimitive(error)
                    ? _this._eventFromRejectionWithPrimitive(error)
                    : eventFromUnknownInput(error, undefined, {
                        attachStacktrace: client && client.getOptions().attachStacktrace,
                        rejection: true,
                    });
                event.level = Severity.Error;
                addExceptionMechanism(event, {
                    handled: false,
                    type: 'onunhandledrejection',
                });
                currentHub.captureEvent(event, {
                    originalException: error,
                });
                return;
            },
            type: 'unhandledrejection',
        });
        this._onUnhandledRejectionHandlerInstalled = true;
    };
    /**
     * This function creates a stack from an old, error-less onerror handler.
     */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    GlobalHandlers.prototype._eventFromIncompleteOnError = function (msg, url, line, column) {
        var ERROR_TYPES_RE = /^(?:[Uu]ncaught (?:exception: )?)?(?:((?:Eval|Internal|Range|Reference|Syntax|Type|URI|)Error): )?(.*)$/i;
        // If 'message' is ErrorEvent, get real message from inside
        var message = isErrorEvent(msg) ? msg.message : msg;
        var name;
        var groups = message.match(ERROR_TYPES_RE);
        if (groups) {
            name = groups[1];
            message = groups[2];
        }
        var event = {
            exception: {
                values: [
                    {
                        type: name || 'Error',
                        value: message,
                    },
                ],
            },
        };
        return this._enhanceEventWithInitialFrame(event, url, line, column);
    };
    /**
     * Create an event from a promise rejection where the `reason` is a primitive.
     *
     * @param reason: The `reason` property of the promise rejection
     * @returns An Event object with an appropriate `exception` value
     */
    GlobalHandlers.prototype._eventFromRejectionWithPrimitive = function (reason) {
        return {
            exception: {
                values: [
                    {
                        type: 'UnhandledRejection',
                        // String() is needed because the Primitive type includes symbols (which can't be automatically stringified)
                        value: "Non-Error promise rejection captured with value: " + String(reason),
                    },
                ],
            },
        };
    };
    /** JSDoc */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    GlobalHandlers.prototype._enhanceEventWithInitialFrame = function (event, url, line, column) {
        event.exception = event.exception || {};
        event.exception.values = event.exception.values || [];
        event.exception.values[0] = event.exception.values[0] || {};
        event.exception.values[0].stacktrace = event.exception.values[0].stacktrace || {};
        event.exception.values[0].stacktrace.frames = event.exception.values[0].stacktrace.frames || [];
        var colno = isNaN(parseInt(column, 10)) ? undefined : column;
        var lineno = isNaN(parseInt(line, 10)) ? undefined : line;
        var filename = isString(url) && url.length > 0 ? url : getLocationHref();
        if (event.exception.values[0].stacktrace.frames.length === 0) {
            event.exception.values[0].stacktrace.frames.push({
                colno: colno,
                filename: filename,
                function: '?',
                in_app: true,
                lineno: lineno,
            });
        }
        return event;
    };
    /**
     * @inheritDoc
     */
    GlobalHandlers.id = 'GlobalHandlers';
    return GlobalHandlers;
}());

var DEFAULT_EVENT_TARGET = [
    'EventTarget',
    'Window',
    'Node',
    'ApplicationCache',
    'AudioTrackList',
    'ChannelMergerNode',
    'CryptoOperation',
    'EventSource',
    'FileReader',
    'HTMLUnknownElement',
    'IDBDatabase',
    'IDBRequest',
    'IDBTransaction',
    'KeyOperation',
    'MediaController',
    'MessagePort',
    'ModalWindow',
    'Notification',
    'SVGElementInstance',
    'Screen',
    'TextTrack',
    'TextTrackCue',
    'TextTrackList',
    'WebSocket',
    'WebSocketWorker',
    'Worker',
    'XMLHttpRequest',
    'XMLHttpRequestEventTarget',
    'XMLHttpRequestUpload',
];
/** Wrap timer functions and event targets to catch errors and provide better meta data */
var TryCatch = /** @class */ (function () {
    /**
     * @inheritDoc
     */
    function TryCatch(options) {
        /**
         * @inheritDoc
         */
        this.name = TryCatch.id;
        this._options = __assign$2({ XMLHttpRequest: true, eventTarget: true, requestAnimationFrame: true, setInterval: true, setTimeout: true }, options);
    }
    /**
     * Wrap timer functions and event targets to catch errors
     * and provide better metadata.
     */
    TryCatch.prototype.setupOnce = function () {
        var global = getGlobalObject();
        if (this._options.setTimeout) {
            fill(global, 'setTimeout', this._wrapTimeFunction.bind(this));
        }
        if (this._options.setInterval) {
            fill(global, 'setInterval', this._wrapTimeFunction.bind(this));
        }
        if (this._options.requestAnimationFrame) {
            fill(global, 'requestAnimationFrame', this._wrapRAF.bind(this));
        }
        if (this._options.XMLHttpRequest && 'XMLHttpRequest' in global) {
            fill(XMLHttpRequest.prototype, 'send', this._wrapXHR.bind(this));
        }
        if (this._options.eventTarget) {
            var eventTarget = Array.isArray(this._options.eventTarget) ? this._options.eventTarget : DEFAULT_EVENT_TARGET;
            eventTarget.forEach(this._wrapEventTarget.bind(this));
        }
    };
    /** JSDoc */
    TryCatch.prototype._wrapTimeFunction = function (original) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var originalCallback = args[0];
            args[0] = wrap(originalCallback, {
                mechanism: {
                    data: { function: getFunctionName(original) },
                    handled: true,
                    type: 'instrument',
                },
            });
            return original.apply(this, args);
        };
    };
    /** JSDoc */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    TryCatch.prototype._wrapRAF = function (original) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return function (callback) {
            // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
            return original.call(this, wrap(callback, {
                mechanism: {
                    data: {
                        function: 'requestAnimationFrame',
                        handler: getFunctionName(original),
                    },
                    handled: true,
                    type: 'instrument',
                },
            }));
        };
    };
    /** JSDoc */
    TryCatch.prototype._wrapEventTarget = function (target) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        var global = getGlobalObject();
        // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
        var proto = global[target] && global[target].prototype;
        // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access, no-prototype-builtins
        if (!proto || !proto.hasOwnProperty || !proto.hasOwnProperty('addEventListener')) {
            return;
        }
        fill(proto, 'addEventListener', function (original) {
            return function (eventName, fn, options) {
                try {
                    if (typeof fn.handleEvent === 'function') {
                        fn.handleEvent = wrap(fn.handleEvent.bind(fn), {
                            mechanism: {
                                data: {
                                    function: 'handleEvent',
                                    handler: getFunctionName(fn),
                                    target: target,
                                },
                                handled: true,
                                type: 'instrument',
                            },
                        });
                    }
                }
                catch (err) {
                    // can sometimes get 'Permission denied to access property "handle Event'
                }
                return original.call(this, eventName, 
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                wrap(fn, {
                    mechanism: {
                        data: {
                            function: 'addEventListener',
                            handler: getFunctionName(fn),
                            target: target,
                        },
                        handled: true,
                        type: 'instrument',
                    },
                }), options);
            };
        });
        fill(proto, 'removeEventListener', function (originalRemoveEventListener) {
            return function (eventName, fn, options) {
                var _a;
                /**
                 * There are 2 possible scenarios here:
                 *
                 * 1. Someone passes a callback, which was attached prior to Sentry initialization, or by using unmodified
                 * method, eg. `document.addEventListener.call(el, name, handler). In this case, we treat this function
                 * as a pass-through, and call original `removeEventListener` with it.
                 *
                 * 2. Someone passes a callback, which was attached after Sentry was initialized, which means that it was using
                 * our wrapped version of `addEventListener`, which internally calls `wrap` helper.
                 * This helper "wraps" whole callback inside a try/catch statement, and attached appropriate metadata to it,
                 * in order for us to make a distinction between wrapped/non-wrapped functions possible.
                 * If a function was wrapped, it has additional property of `__sentry_wrapped__`, holding the handler.
                 *
                 * When someone adds a handler prior to initialization, and then do it again, but after,
                 * then we have to detach both of them. Otherwise, if we'd detach only wrapped one, it'd be impossible
                 * to get rid of the initial handler and it'd stick there forever.
                 */
                var wrappedEventHandler = fn;
                try {
                    var originalEventHandler = (_a = wrappedEventHandler) === null || _a === void 0 ? void 0 : _a.__sentry_wrapped__;
                    if (originalEventHandler) {
                        originalRemoveEventListener.call(this, eventName, originalEventHandler, options);
                    }
                }
                catch (e) {
                    // ignore, accessing __sentry_wrapped__ will throw in some Selenium environments
                }
                return originalRemoveEventListener.call(this, eventName, wrappedEventHandler, options);
            };
        });
    };
    /** JSDoc */
    TryCatch.prototype._wrapXHR = function (originalSend) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            // eslint-disable-next-line @typescript-eslint/no-this-alias
            var xhr = this;
            var xmlHttpRequestProps = ['onload', 'onerror', 'onprogress', 'onreadystatechange'];
            xmlHttpRequestProps.forEach(function (prop) {
                if (prop in xhr && typeof xhr[prop] === 'function') {
                    // eslint-disable-next-line @typescript-eslint/no-explicit-any
                    fill(xhr, prop, function (original) {
                        var wrapOptions = {
                            mechanism: {
                                data: {
                                    function: prop,
                                    handler: getFunctionName(original),
                                },
                                handled: true,
                                type: 'instrument',
                            },
                        };
                        // If Instrument integration has been called before TryCatch, get the name of original function
                        if (original.__sentry_original__) {
                            wrapOptions.mechanism.data.handler = getFunctionName(original.__sentry_original__);
                        }
                        // Otherwise wrap directly
                        return wrap(original, wrapOptions);
                    });
                }
            });
            return originalSend.apply(this, args);
        };
    };
    /**
     * @inheritDoc
     */
    TryCatch.id = 'TryCatch';
    return TryCatch;
}());

/**
 * Default Breadcrumbs instrumentations
 * TODO: Deprecated - with v6, this will be renamed to `Instrument`
 */
var Breadcrumbs = /** @class */ (function () {
    /**
     * @inheritDoc
     */
    function Breadcrumbs(options) {
        /**
         * @inheritDoc
         */
        this.name = Breadcrumbs.id;
        this._options = __assign$2({ console: true, dom: true, fetch: true, history: true, sentry: true, xhr: true }, options);
    }
    /**
     * Create a breadcrumb of `sentry` from the events themselves
     */
    Breadcrumbs.prototype.addSentryBreadcrumb = function (event) {
        if (!this._options.sentry) {
            return;
        }
        getCurrentHub().addBreadcrumb({
            category: "sentry." + (event.type === 'transaction' ? 'transaction' : 'event'),
            event_id: event.event_id,
            level: event.level,
            message: getEventDescription(event),
        }, {
            event: event,
        });
    };
    /**
     * Instrument browser built-ins w/ breadcrumb capturing
     *  - Console API
     *  - DOM API (click/typing)
     *  - XMLHttpRequest API
     *  - Fetch API
     *  - History API
     */
    Breadcrumbs.prototype.setupOnce = function () {
        var _this = this;
        if (this._options.console) {
            addInstrumentationHandler({
                callback: function () {
                    var args = [];
                    for (var _i = 0; _i < arguments.length; _i++) {
                        args[_i] = arguments[_i];
                    }
                    _this._consoleBreadcrumb.apply(_this, __spread$2(args));
                },
                type: 'console',
            });
        }
        if (this._options.dom) {
            addInstrumentationHandler({
                callback: function () {
                    var args = [];
                    for (var _i = 0; _i < arguments.length; _i++) {
                        args[_i] = arguments[_i];
                    }
                    _this._domBreadcrumb.apply(_this, __spread$2(args));
                },
                type: 'dom',
            });
        }
        if (this._options.xhr) {
            addInstrumentationHandler({
                callback: function () {
                    var args = [];
                    for (var _i = 0; _i < arguments.length; _i++) {
                        args[_i] = arguments[_i];
                    }
                    _this._xhrBreadcrumb.apply(_this, __spread$2(args));
                },
                type: 'xhr',
            });
        }
        if (this._options.fetch) {
            addInstrumentationHandler({
                callback: function () {
                    var args = [];
                    for (var _i = 0; _i < arguments.length; _i++) {
                        args[_i] = arguments[_i];
                    }
                    _this._fetchBreadcrumb.apply(_this, __spread$2(args));
                },
                type: 'fetch',
            });
        }
        if (this._options.history) {
            addInstrumentationHandler({
                callback: function () {
                    var args = [];
                    for (var _i = 0; _i < arguments.length; _i++) {
                        args[_i] = arguments[_i];
                    }
                    _this._historyBreadcrumb.apply(_this, __spread$2(args));
                },
                type: 'history',
            });
        }
    };
    /**
     * Creates breadcrumbs from console API calls
     */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    Breadcrumbs.prototype._consoleBreadcrumb = function (handlerData) {
        var breadcrumb = {
            category: 'console',
            data: {
                arguments: handlerData.args,
                logger: 'console',
            },
            level: Severity.fromString(handlerData.level),
            message: safeJoin(handlerData.args, ' '),
        };
        if (handlerData.level === 'assert') {
            if (handlerData.args[0] === false) {
                breadcrumb.message = "Assertion failed: " + (safeJoin(handlerData.args.slice(1), ' ') || 'console.assert');
                breadcrumb.data.arguments = handlerData.args.slice(1);
            }
            else {
                // Don't capture a breadcrumb for passed assertions
                return;
            }
        }
        getCurrentHub().addBreadcrumb(breadcrumb, {
            input: handlerData.args,
            level: handlerData.level,
        });
    };
    /**
     * Creates breadcrumbs from DOM API calls
     */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    Breadcrumbs.prototype._domBreadcrumb = function (handlerData) {
        var target;
        var keyAttrs = typeof this._options.dom === 'object' ? this._options.dom.serializeAttribute : undefined;
        if (typeof keyAttrs === 'string') {
            keyAttrs = [keyAttrs];
        }
        // Accessing event.target can throw (see getsentry/raven-js#838, #768)
        try {
            target = handlerData.event.target
                ? htmlTreeAsString(handlerData.event.target, keyAttrs)
                : htmlTreeAsString(handlerData.event, keyAttrs);
        }
        catch (e) {
            target = '<unknown>';
        }
        if (target.length === 0) {
            return;
        }
        getCurrentHub().addBreadcrumb({
            category: "ui." + handlerData.name,
            message: target,
        }, {
            event: handlerData.event,
            name: handlerData.name,
            global: handlerData.global,
        });
    };
    /**
     * Creates breadcrumbs from XHR API calls
     */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    Breadcrumbs.prototype._xhrBreadcrumb = function (handlerData) {
        if (handlerData.endTimestamp) {
            // We only capture complete, non-sentry requests
            if (handlerData.xhr.__sentry_own_request__) {
                return;
            }
            var _a = handlerData.xhr.__sentry_xhr__ || {}, method = _a.method, url = _a.url, status_code = _a.status_code, body = _a.body;
            getCurrentHub().addBreadcrumb({
                category: 'xhr',
                data: {
                    method: method,
                    url: url,
                    status_code: status_code,
                },
                type: 'http',
            }, {
                xhr: handlerData.xhr,
                input: body,
            });
            return;
        }
    };
    /**
     * Creates breadcrumbs from fetch API calls
     */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    Breadcrumbs.prototype._fetchBreadcrumb = function (handlerData) {
        // We only capture complete fetch requests
        if (!handlerData.endTimestamp) {
            return;
        }
        if (handlerData.fetchData.url.match(/sentry_key/) && handlerData.fetchData.method === 'POST') {
            // We will not create breadcrumbs for fetch requests that contain `sentry_key` (internal sentry requests)
            return;
        }
        if (handlerData.error) {
            getCurrentHub().addBreadcrumb({
                category: 'fetch',
                data: handlerData.fetchData,
                level: Severity.Error,
                type: 'http',
            }, {
                data: handlerData.error,
                input: handlerData.args,
            });
        }
        else {
            getCurrentHub().addBreadcrumb({
                category: 'fetch',
                data: __assign$2(__assign$2({}, handlerData.fetchData), { status_code: handlerData.response.status }),
                type: 'http',
            }, {
                input: handlerData.args,
                response: handlerData.response,
            });
        }
    };
    /**
     * Creates breadcrumbs from history API calls
     */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    Breadcrumbs.prototype._historyBreadcrumb = function (handlerData) {
        var global = getGlobalObject();
        var from = handlerData.from;
        var to = handlerData.to;
        var parsedLoc = parseUrl(global.location.href);
        var parsedFrom = parseUrl(from);
        var parsedTo = parseUrl(to);
        // Initial pushState doesn't provide `from` information
        if (!parsedFrom.path) {
            parsedFrom = parsedLoc;
        }
        // Use only the path component of the URL if the URL matches the current
        // document (almost all the time when using pushState)
        if (parsedLoc.protocol === parsedTo.protocol && parsedLoc.host === parsedTo.host) {
            to = parsedTo.relative;
        }
        if (parsedLoc.protocol === parsedFrom.protocol && parsedLoc.host === parsedFrom.host) {
            from = parsedFrom.relative;
        }
        getCurrentHub().addBreadcrumb({
            category: 'navigation',
            data: {
                from: from,
                to: to,
            },
        });
    };
    /**
     * @inheritDoc
     */
    Breadcrumbs.id = 'Breadcrumbs';
    return Breadcrumbs;
}());

var DEFAULT_KEY = 'cause';
var DEFAULT_LIMIT = 5;
/** Adds SDK info to an event. */
var LinkedErrors = /** @class */ (function () {
    /**
     * @inheritDoc
     */
    function LinkedErrors(options) {
        if (options === void 0) { options = {}; }
        /**
         * @inheritDoc
         */
        this.name = LinkedErrors.id;
        this._key = options.key || DEFAULT_KEY;
        this._limit = options.limit || DEFAULT_LIMIT;
    }
    /**
     * @inheritDoc
     */
    LinkedErrors.prototype.setupOnce = function () {
        addGlobalEventProcessor(function (event, hint) {
            var self = getCurrentHub().getIntegration(LinkedErrors);
            if (self) {
                var handler = self._handler && self._handler.bind(self);
                return typeof handler === 'function' ? handler(event, hint) : event;
            }
            return event;
        });
    };
    /**
     * @inheritDoc
     */
    LinkedErrors.prototype._handler = function (event, hint) {
        if (!event.exception || !event.exception.values || !hint || !isInstanceOf(hint.originalException, Error)) {
            return event;
        }
        var linkedErrors = this._walkErrorTree(hint.originalException, this._key);
        event.exception.values = __spread$2(linkedErrors, event.exception.values);
        return event;
    };
    /**
     * @inheritDoc
     */
    LinkedErrors.prototype._walkErrorTree = function (error, key, stack) {
        if (stack === void 0) { stack = []; }
        if (!isInstanceOf(error[key], Error) || stack.length + 1 >= this._limit) {
            return stack;
        }
        var stacktrace = computeStackTrace(error[key]);
        var exception = exceptionFromStacktrace(stacktrace);
        return this._walkErrorTree(error[key], key, __spread$2([exception], stack));
    };
    /**
     * @inheritDoc
     */
    LinkedErrors.id = 'LinkedErrors';
    return LinkedErrors;
}());

var global = getGlobalObject();
/** UserAgent */
var UserAgent = /** @class */ (function () {
    function UserAgent() {
        /**
         * @inheritDoc
         */
        this.name = UserAgent.id;
    }
    /**
     * @inheritDoc
     */
    UserAgent.prototype.setupOnce = function () {
        addGlobalEventProcessor(function (event) {
            var _a, _b, _c;
            if (getCurrentHub().getIntegration(UserAgent)) {
                // if none of the information we want exists, don't bother
                if (!global.navigator && !global.location && !global.document) {
                    return event;
                }
                // grab as much info as exists and add it to the event
                var url = ((_a = event.request) === null || _a === void 0 ? void 0 : _a.url) || ((_b = global.location) === null || _b === void 0 ? void 0 : _b.href);
                var referrer = (global.document || {}).referrer;
                var userAgent = (global.navigator || {}).userAgent;
                var headers = __assign$2(__assign$2(__assign$2({}, (_c = event.request) === null || _c === void 0 ? void 0 : _c.headers), (referrer && { Referer: referrer })), (userAgent && { 'User-Agent': userAgent }));
                var request = __assign$2(__assign$2({}, (url && { url: url })), { headers: headers });
                return __assign$2(__assign$2({}, event), { request: request });
            }
            return event;
        });
    };
    /**
     * @inheritDoc
     */
    UserAgent.id = 'UserAgent';
    return UserAgent;
}());

/** Deduplication filter */
var Dedupe = /** @class */ (function () {
    function Dedupe() {
        /**
         * @inheritDoc
         */
        this.name = Dedupe.id;
    }
    /**
     * @inheritDoc
     */
    Dedupe.prototype.setupOnce = function (addGlobalEventProcessor, getCurrentHub) {
        addGlobalEventProcessor(function (currentEvent) {
            var self = getCurrentHub().getIntegration(Dedupe);
            if (self) {
                // Juuust in case something goes wrong
                try {
                    if (self._shouldDropEvent(currentEvent, self._previousEvent)) {
                        logger.warn("Event dropped due to being a duplicate of previously captured event.");
                        return null;
                    }
                }
                catch (_oO) {
                    return (self._previousEvent = currentEvent);
                }
                return (self._previousEvent = currentEvent);
            }
            return currentEvent;
        });
    };
    /** JSDoc */
    Dedupe.prototype._shouldDropEvent = function (currentEvent, previousEvent) {
        if (!previousEvent) {
            return false;
        }
        if (this._isSameMessageEvent(currentEvent, previousEvent)) {
            return true;
        }
        if (this._isSameExceptionEvent(currentEvent, previousEvent)) {
            return true;
        }
        return false;
    };
    /** JSDoc */
    Dedupe.prototype._isSameMessageEvent = function (currentEvent, previousEvent) {
        var currentMessage = currentEvent.message;
        var previousMessage = previousEvent.message;
        // If neither event has a message property, they were both exceptions, so bail out
        if (!currentMessage && !previousMessage) {
            return false;
        }
        // If only one event has a stacktrace, but not the other one, they are not the same
        if ((currentMessage && !previousMessage) || (!currentMessage && previousMessage)) {
            return false;
        }
        if (currentMessage !== previousMessage) {
            return false;
        }
        if (!this._isSameFingerprint(currentEvent, previousEvent)) {
            return false;
        }
        if (!this._isSameStacktrace(currentEvent, previousEvent)) {
            return false;
        }
        return true;
    };
    /** JSDoc */
    Dedupe.prototype._getFramesFromEvent = function (event) {
        var exception = event.exception;
        if (exception) {
            try {
                // @ts-ignore Object could be undefined
                return exception.values[0].stacktrace.frames;
            }
            catch (_oO) {
                return undefined;
            }
        }
        else if (event.stacktrace) {
            return event.stacktrace.frames;
        }
        return undefined;
    };
    /** JSDoc */
    Dedupe.prototype._isSameStacktrace = function (currentEvent, previousEvent) {
        var currentFrames = this._getFramesFromEvent(currentEvent);
        var previousFrames = this._getFramesFromEvent(previousEvent);
        // If neither event has a stacktrace, they are assumed to be the same
        if (!currentFrames && !previousFrames) {
            return true;
        }
        // If only one event has a stacktrace, but not the other one, they are not the same
        if ((currentFrames && !previousFrames) || (!currentFrames && previousFrames)) {
            return false;
        }
        currentFrames = currentFrames;
        previousFrames = previousFrames;
        // If number of frames differ, they are not the same
        if (previousFrames.length !== currentFrames.length) {
            return false;
        }
        // Otherwise, compare the two
        for (var i = 0; i < previousFrames.length; i++) {
            var frameA = previousFrames[i];
            var frameB = currentFrames[i];
            if (frameA.filename !== frameB.filename ||
                frameA.lineno !== frameB.lineno ||
                frameA.colno !== frameB.colno ||
                frameA.function !== frameB.function) {
                return false;
            }
        }
        return true;
    };
    /** JSDoc */
    Dedupe.prototype._getExceptionFromEvent = function (event) {
        return event.exception && event.exception.values && event.exception.values[0];
    };
    /** JSDoc */
    Dedupe.prototype._isSameExceptionEvent = function (currentEvent, previousEvent) {
        var previousException = this._getExceptionFromEvent(previousEvent);
        var currentException = this._getExceptionFromEvent(currentEvent);
        if (!previousException || !currentException) {
            return false;
        }
        if (previousException.type !== currentException.type || previousException.value !== currentException.value) {
            return false;
        }
        if (!this._isSameFingerprint(currentEvent, previousEvent)) {
            return false;
        }
        if (!this._isSameStacktrace(currentEvent, previousEvent)) {
            return false;
        }
        return true;
    };
    /** JSDoc */
    Dedupe.prototype._isSameFingerprint = function (currentEvent, previousEvent) {
        var currentFingerprint = currentEvent.fingerprint;
        var previousFingerprint = previousEvent.fingerprint;
        // If neither event has a fingerprint, they are assumed to be the same
        if (!currentFingerprint && !previousFingerprint) {
            return true;
        }
        // If only one event has a fingerprint, but not the other one, they are not the same
        if ((currentFingerprint && !previousFingerprint) || (!currentFingerprint && previousFingerprint)) {
            return false;
        }
        currentFingerprint = currentFingerprint;
        previousFingerprint = previousFingerprint;
        // Otherwise, compare the two
        try {
            return !!(currentFingerprint.join('') === previousFingerprint.join(''));
        }
        catch (_oO) {
            return false;
        }
    };
    /**
     * @inheritDoc
     */
    Dedupe.id = 'Dedupe';
    return Dedupe;
}());

/**
 * The Sentry Browser SDK Client.
 *
 * @see BrowserOptions for documentation on configuration options.
 * @see SentryClient for usage documentation.
 */
var BrowserClient = /** @class */ (function (_super) {
    __extends$1(BrowserClient, _super);
    /**
     * Creates a new Browser SDK instance.
     *
     * @param options Configuration options for this SDK.
     */
    function BrowserClient(options) {
        if (options === void 0) { options = {}; }
        var _this = this;
        options._metadata = options._metadata || {};
        options._metadata.sdk = options._metadata.sdk || {
            name: 'sentry.javascript.browser',
            packages: [
                {
                    name: 'npm:@sentry/browser',
                    version: SDK_VERSION,
                },
            ],
            version: SDK_VERSION,
        };
        _this = _super.call(this, BrowserBackend, options) || this;
        return _this;
    }
    /**
     * Show a report dialog to the user to send feedback to a specific event.
     *
     * @param options Set individual options for the dialog
     */
    BrowserClient.prototype.showReportDialog = function (options) {
        if (options === void 0) { options = {}; }
        // doesn't work without a document (React Native)
        var document = getGlobalObject().document;
        if (!document) {
            return;
        }
        if (!this._isEnabled()) {
            logger.error('Trying to call showReportDialog with Sentry Client disabled');
            return;
        }
        injectReportDialog(__assign$2(__assign$2({}, options), { dsn: options.dsn || this.getDsn() }));
    };
    /**
     * @inheritDoc
     */
    BrowserClient.prototype._prepareEvent = function (event, scope, hint) {
        event.platform = event.platform || 'javascript';
        return _super.prototype._prepareEvent.call(this, event, scope, hint);
    };
    /**
     * @inheritDoc
     */
    BrowserClient.prototype._sendEvent = function (event) {
        var integration = this.getIntegration(Breadcrumbs);
        if (integration) {
            integration.addSentryBreadcrumb(event);
        }
        _super.prototype._sendEvent.call(this, event);
    };
    return BrowserClient;
}(BaseClient));

var defaultIntegrations = [
    new InboundFilters(),
    new FunctionToString(),
    new TryCatch(),
    new Breadcrumbs(),
    new GlobalHandlers(),
    new LinkedErrors(),
    new Dedupe(),
    new UserAgent(),
];
/**
 * The Sentry Browser SDK Client.
 *
 * To use this SDK, call the {@link init} function as early as possible when
 * loading the web page. To set context information or send manual events, use
 * the provided methods.
 *
 * @example
 *
 * ```
 *
 * import { init } from '@sentry/browser';
 *
 * init({
 *   dsn: '__DSN__',
 *   // ...
 * });
 * ```
 *
 * @example
 * ```
 *
 * import { configureScope } from '@sentry/browser';
 * configureScope((scope: Scope) => {
 *   scope.setExtra({ battery: 0.7 });
 *   scope.setTag({ user_mode: 'admin' });
 *   scope.setUser({ id: '4711' });
 * });
 * ```
 *
 * @example
 * ```
 *
 * import { addBreadcrumb } from '@sentry/browser';
 * addBreadcrumb({
 *   message: 'My Breadcrumb',
 *   // ...
 * });
 * ```
 *
 * @example
 *
 * ```
 *
 * import * as Sentry from '@sentry/browser';
 * Sentry.captureMessage('Hello, world!');
 * Sentry.captureException(new Error('Good bye'));
 * Sentry.captureEvent({
 *   message: 'Manual',
 *   stacktrace: [
 *     // ...
 *   ],
 * });
 * ```
 *
 * @see {@link BrowserOptions} for documentation on configuration options.
 */
function init(options) {
    if (options === void 0) { options = {}; }
    if (options.defaultIntegrations === undefined) {
        options.defaultIntegrations = defaultIntegrations;
    }
    if (options.release === undefined) {
        var window_1 = getGlobalObject();
        // This supports the variable that sentry-webpack-plugin injects
        if (window_1.SENTRY_RELEASE && window_1.SENTRY_RELEASE.id) {
            options.release = window_1.SENTRY_RELEASE.id;
        }
    }
    if (options.autoSessionTracking === undefined) {
        options.autoSessionTracking = true;
    }
    if (options.sendClientReports === undefined) {
        options.sendClientReports = true;
    }
    initAndBind(BrowserClient, options);
    if (options.autoSessionTracking) {
        startSessionTracking();
    }
}
/**
 * Enable automatic Session Tracking for the initial page load.
 */
function startSessionTracking() {
    var window = getGlobalObject();
    var document = window.document;
    if (typeof document === 'undefined') {
        logger.warn('Session tracking in non-browser environment with @sentry/browser is not supported.');
        return;
    }
    var hub = getCurrentHub();
    // The only way for this to be false is for there to be a version mismatch between @sentry/browser (>= 6.0.0) and
    // @sentry/hub (< 5.27.0). In the simple case, there won't ever be such a mismatch, because the two packages are
    // pinned at the same version in package.json, but there are edge cases where it's possible. See
    // https://github.com/getsentry/sentry-javascript/issues/3207 and
    // https://github.com/getsentry/sentry-javascript/issues/3234 and
    // https://github.com/getsentry/sentry-javascript/issues/3278.
    if (typeof hub.startSession !== 'function' || typeof hub.captureSession !== 'function') {
        return;
    }
    // The session duration for browser sessions does not track a meaningful
    // concept that can be used as a metric.
    // Automatically captured sessions are akin to page views, and thus we
    // discard their duration.
    hub.startSession({ ignoreDuration: true });
    hub.captureSession();
    // We want to create a session for every navigation as well
    addInstrumentationHandler({
        callback: function (_a) {
            var from = _a.from, to = _a.to;
            // Don't create an additional session for the initial route or if the location did not change
            if (from === undefined || from === to) {
                return;
            }
            hub.startSession({ ignoreDuration: true });
            hub.captureSession();
        },
        type: 'history',
    });
}

/**
 *  base64.ts
 *
 *  Licensed under the BSD 3-Clause License.
 *    http://opensource.org/licenses/BSD-3-Clause
 *
 *  References:
 *    http://en.wikipedia.org/wiki/Base64
 *
 * @author Dan Kogai (https://github.com/dankogai)
 */
const version = '3.7.2';
/**
 * @deprecated use lowercase `version`.
 */
const VERSION = version;
const _hasatob = typeof atob === 'function';
const _hasbtoa = typeof btoa === 'function';
const _hasBuffer = typeof Buffer === 'function';
const _TD = typeof TextDecoder === 'function' ? new TextDecoder() : undefined;
const _TE = typeof TextEncoder === 'function' ? new TextEncoder() : undefined;
const b64ch = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
const b64chs = Array.prototype.slice.call(b64ch);
const b64tab = ((a) => {
    let tab = {};
    a.forEach((c, i) => tab[c] = i);
    return tab;
})(b64chs);
const b64re = /^(?:[A-Za-z\d+\/]{4})*?(?:[A-Za-z\d+\/]{2}(?:==)?|[A-Za-z\d+\/]{3}=?)?$/;
const _fromCC = String.fromCharCode.bind(String);
const _U8Afrom = typeof Uint8Array.from === 'function'
    ? Uint8Array.from.bind(Uint8Array)
    : (it, fn = (x) => x) => new Uint8Array(Array.prototype.slice.call(it, 0).map(fn));
const _mkUriSafe = (src) => src
    .replace(/=/g, '').replace(/[+\/]/g, (m0) => m0 == '+' ? '-' : '_');
const _tidyB64 = (s) => s.replace(/[^A-Za-z0-9\+\/]/g, '');
/**
 * polyfill version of `btoa`
 */
const btoaPolyfill = (bin) => {
    // console.log('polyfilled');
    let u32, c0, c1, c2, asc = '';
    const pad = bin.length % 3;
    for (let i = 0; i < bin.length;) {
        if ((c0 = bin.charCodeAt(i++)) > 255 ||
            (c1 = bin.charCodeAt(i++)) > 255 ||
            (c2 = bin.charCodeAt(i++)) > 255)
            throw new TypeError('invalid character found');
        u32 = (c0 << 16) | (c1 << 8) | c2;
        asc += b64chs[u32 >> 18 & 63]
            + b64chs[u32 >> 12 & 63]
            + b64chs[u32 >> 6 & 63]
            + b64chs[u32 & 63];
    }
    return pad ? asc.slice(0, pad - 3) + "===".substring(pad) : asc;
};
/**
 * does what `window.btoa` of web browsers do.
 * @param {String} bin binary string
 * @returns {string} Base64-encoded string
 */
const _btoa = _hasbtoa ? (bin) => btoa(bin)
    : _hasBuffer ? (bin) => Buffer.from(bin, 'binary').toString('base64')
        : btoaPolyfill;
const _fromUint8Array = _hasBuffer
    ? (u8a) => Buffer.from(u8a).toString('base64')
    : (u8a) => {
        // cf. https://stackoverflow.com/questions/12710001/how-to-convert-uint8-array-to-base64-encoded-string/12713326#12713326
        const maxargs = 0x1000;
        let strs = [];
        for (let i = 0, l = u8a.length; i < l; i += maxargs) {
            strs.push(_fromCC.apply(null, u8a.subarray(i, i + maxargs)));
        }
        return _btoa(strs.join(''));
    };
/**
 * converts a Uint8Array to a Base64 string.
 * @param {boolean} [urlsafe] URL-and-filename-safe a la RFC4648 §5
 * @returns {string} Base64 string
 */
const fromUint8Array = (u8a, urlsafe = false) => urlsafe ? _mkUriSafe(_fromUint8Array(u8a)) : _fromUint8Array(u8a);
// This trick is found broken https://github.com/dankogai/js-base64/issues/130
// const utob = (src: string) => unescape(encodeURIComponent(src));
// reverting good old fationed regexp
const cb_utob = (c) => {
    if (c.length < 2) {
        var cc = c.charCodeAt(0);
        return cc < 0x80 ? c
            : cc < 0x800 ? (_fromCC(0xc0 | (cc >>> 6))
                + _fromCC(0x80 | (cc & 0x3f)))
                : (_fromCC(0xe0 | ((cc >>> 12) & 0x0f))
                    + _fromCC(0x80 | ((cc >>> 6) & 0x3f))
                    + _fromCC(0x80 | (cc & 0x3f)));
    }
    else {
        var cc = 0x10000
            + (c.charCodeAt(0) - 0xD800) * 0x400
            + (c.charCodeAt(1) - 0xDC00);
        return (_fromCC(0xf0 | ((cc >>> 18) & 0x07))
            + _fromCC(0x80 | ((cc >>> 12) & 0x3f))
            + _fromCC(0x80 | ((cc >>> 6) & 0x3f))
            + _fromCC(0x80 | (cc & 0x3f)));
    }
};
const re_utob = /[\uD800-\uDBFF][\uDC00-\uDFFFF]|[^\x00-\x7F]/g;
/**
 * @deprecated should have been internal use only.
 * @param {string} src UTF-8 string
 * @returns {string} UTF-16 string
 */
const utob = (u) => u.replace(re_utob, cb_utob);
//
const _encode = _hasBuffer
    ? (s) => Buffer.from(s, 'utf8').toString('base64')
    : _TE
        ? (s) => _fromUint8Array(_TE.encode(s))
        : (s) => _btoa(utob(s));
/**
 * converts a UTF-8-encoded string to a Base64 string.
 * @param {boolean} [urlsafe] if `true` make the result URL-safe
 * @returns {string} Base64 string
 */
const encode = (src, urlsafe = false) => urlsafe
    ? _mkUriSafe(_encode(src))
    : _encode(src);
/**
 * converts a UTF-8-encoded string to URL-safe Base64 RFC4648 §5.
 * @returns {string} Base64 string
 */
const encodeURI = (src) => encode(src, true);
// This trick is found broken https://github.com/dankogai/js-base64/issues/130
// const btou = (src: string) => decodeURIComponent(escape(src));
// reverting good old fationed regexp
const re_btou = /[\xC0-\xDF][\x80-\xBF]|[\xE0-\xEF][\x80-\xBF]{2}|[\xF0-\xF7][\x80-\xBF]{3}/g;
const cb_btou = (cccc) => {
    switch (cccc.length) {
        case 4:
            var cp = ((0x07 & cccc.charCodeAt(0)) << 18)
                | ((0x3f & cccc.charCodeAt(1)) << 12)
                | ((0x3f & cccc.charCodeAt(2)) << 6)
                | (0x3f & cccc.charCodeAt(3)), offset = cp - 0x10000;
            return (_fromCC((offset >>> 10) + 0xD800)
                + _fromCC((offset & 0x3FF) + 0xDC00));
        case 3:
            return _fromCC(((0x0f & cccc.charCodeAt(0)) << 12)
                | ((0x3f & cccc.charCodeAt(1)) << 6)
                | (0x3f & cccc.charCodeAt(2)));
        default:
            return _fromCC(((0x1f & cccc.charCodeAt(0)) << 6)
                | (0x3f & cccc.charCodeAt(1)));
    }
};
/**
 * @deprecated should have been internal use only.
 * @param {string} src UTF-16 string
 * @returns {string} UTF-8 string
 */
const btou = (b) => b.replace(re_btou, cb_btou);
/**
 * polyfill version of `atob`
 */
const atobPolyfill = (asc) => {
    // console.log('polyfilled');
    asc = asc.replace(/\s+/g, '');
    if (!b64re.test(asc))
        throw new TypeError('malformed base64.');
    asc += '=='.slice(2 - (asc.length & 3));
    let u24, bin = '', r1, r2;
    for (let i = 0; i < asc.length;) {
        u24 = b64tab[asc.charAt(i++)] << 18
            | b64tab[asc.charAt(i++)] << 12
            | (r1 = b64tab[asc.charAt(i++)]) << 6
            | (r2 = b64tab[asc.charAt(i++)]);
        bin += r1 === 64 ? _fromCC(u24 >> 16 & 255)
            : r2 === 64 ? _fromCC(u24 >> 16 & 255, u24 >> 8 & 255)
                : _fromCC(u24 >> 16 & 255, u24 >> 8 & 255, u24 & 255);
    }
    return bin;
};
/**
 * does what `window.atob` of web browsers do.
 * @param {String} asc Base64-encoded string
 * @returns {string} binary string
 */
const _atob = _hasatob ? (asc) => atob(_tidyB64(asc))
    : _hasBuffer ? (asc) => Buffer.from(asc, 'base64').toString('binary')
        : atobPolyfill;
//
const _toUint8Array = _hasBuffer
    ? (a) => _U8Afrom(Buffer.from(a, 'base64'))
    : (a) => _U8Afrom(_atob(a), c => c.charCodeAt(0));
/**
 * converts a Base64 string to a Uint8Array.
 */
const toUint8Array = (a) => _toUint8Array(_unURI(a));
//
const _decode = _hasBuffer
    ? (a) => Buffer.from(a, 'base64').toString('utf8')
    : _TD
        ? (a) => _TD.decode(_toUint8Array(a))
        : (a) => btou(_atob(a));
const _unURI = (a) => _tidyB64(a.replace(/[-_]/g, (m0) => m0 == '-' ? '+' : '/'));
/**
 * converts a Base64 string to a UTF-8 string.
 * @param {String} src Base64 string.  Both normal and URL-safe are supported
 * @returns {string} UTF-8 string
 */
const decode = (src) => _decode(_unURI(src));
/**
 * check if a value is a valid Base64 string
 * @param {String} src a value to check
  */
const isValid = (src) => {
    if (typeof src !== 'string')
        return false;
    const s = src.replace(/\s+/g, '').replace(/={0,2}$/, '');
    return !/[^\s0-9a-zA-Z\+/]/.test(s) || !/[^\s0-9a-zA-Z\-_]/.test(s);
};
//
const _noEnum = (v) => {
    return {
        value: v, enumerable: false, writable: true, configurable: true
    };
};
/**
 * extend String.prototype with relevant methods
 */
const extendString = function () {
    const _add = (name, body) => Object.defineProperty(String.prototype, name, _noEnum(body));
    _add('fromBase64', function () { return decode(this); });
    _add('toBase64', function (urlsafe) { return encode(this, urlsafe); });
    _add('toBase64URI', function () { return encode(this, true); });
    _add('toBase64URL', function () { return encode(this, true); });
    _add('toUint8Array', function () { return toUint8Array(this); });
};
/**
 * extend Uint8Array.prototype with relevant methods
 */
const extendUint8Array = function () {
    const _add = (name, body) => Object.defineProperty(Uint8Array.prototype, name, _noEnum(body));
    _add('toBase64', function (urlsafe) { return fromUint8Array(this, urlsafe); });
    _add('toBase64URI', function () { return fromUint8Array(this, true); });
    _add('toBase64URL', function () { return fromUint8Array(this, true); });
};
/**
 * extend Builtin prototypes with relevant methods
 */
const extendBuiltins = () => {
    extendString();
    extendUint8Array();
};
const gBase64 = {
    version: version,
    VERSION: VERSION,
    atob: _atob,
    atobPolyfill: atobPolyfill,
    btoa: _btoa,
    btoaPolyfill: btoaPolyfill,
    fromBase64: decode,
    toBase64: encode,
    encode: encode,
    encodeURI: encodeURI,
    encodeURL: encodeURI,
    utob: utob,
    btou: btou,
    decode: decode,
    isValid: isValid,
    fromUint8Array: fromUint8Array,
    toUint8Array: toUint8Array,
    extendString: extendString,
    extendUint8Array: extendUint8Array,
    extendBuiltins: extendBuiltins,
};

/* Helper Functions
–––––––––––––––––––––––––––––––––––––––––––––––––– */

async function request(options, skipAuth) {
  if (!skipAuth) options.data.access_token = await getAccessToken();
  options.data.consumer_key = CONSUMER_KEY;
  const headers = new Headers({
    'X-Accept': 'application/json',
    'Content-Type': 'application/json'
  }); //?? Is there any way to access this anymore since we no longer use cookie/local storage
  //?? We never set this parameter anywhere; propose we delete this block

  const serverAuth = await getSetting('base_server_auth');

  if (serverAuth) {
    headers.append('Authorization', 'Basic ' + gBase64.encode(serverAuth));
  }

  const fetchSettings = {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(options.data)
  };
  return fetch(API_URL + options.path, fetchSettings).then(handleErrors).then(handleSuccess);
}

function handleErrors(response) {
  const xErrorCode = response.headers.get('x-error-code');
  const xError = response.headers.get('x-error'); // We can reject with the error code and message for better handling

  if (!response.ok) return Promise.reject({
    xErrorCode,
    xError
  });
  return response;
}

function handleSuccess(response) {
  return response ? response.json() : false;
}

/* API CALLS - Should return promises
–––––––––––––––––––––––––––––––––––––––––––––––––– */

function saveToPocket(saveObject) {
  return request({
    path: 'send/',
    data: {
      actions: [{
        action: 'add',
        url: saveObject.url,
        title: saveObject.title,
        ...saveObject.actionInfo,
        ...saveObject.additionalParams
      }]
    }
  }).then(response => {
    return response ? {
      saveObject,
      status: 'ok',
      response: response.action_results[0]
    } : undefined;
  });
}

/* API CALLS - Should return promises
–––––––––––––––––––––––––––––––––––––––––––––––––– */

function getOnSaveTags(url) {
  return request({
    path: 'suggested_tags/',
    data: {
      url,
      version: 2
    }
  }).then(response => response);
}
function syncItemTags(id, tags, actionInfo) {
  return request({
    path: 'send/',
    data: {
      actions: [{
        action: 'tags_replace',
        item_id: id,
        tags,
        ...actionInfo
      }]
    }
  }).then(response => {
    return response ? {
      status: 'ok',
      response: response.action_results[0]
    } : undefined;
  });
}
function fetchStoredTags(since) {
  return request({
    path: 'get/',
    data: {
      tags: 1,
      taglist: 1,
      forcetaglist: 1,
      account: 1,
      since: since ? since : 0
    }
  }).then(response => response);
}

/* API CALLS - Should return promises
–––––––––––––––––––––––––––––––––––––––––––––––––– */

function removeItem(itemId) {
  return request({
    path: 'send/',
    data: {
      actions: [{
        action: 'delete',
        item_id: itemId,
        type: 'page'
      }]
    }
  }).then(response => {
    return response ? {
      status: 'ok',
      response: response.action_results[0]
    } : undefined;
  });
}

/* API CALLS - Should return promises
–––––––––––––––––––––––––––––––––––––––––––––––––– */

function authorize(guid, userCookies) {
  return request({
    path: 'oauth/authorize/',
    data: {
      guid,
      token: userCookies.token,
      user_id: userCookies.userId,
      account: '1',
      grant_type: 'extension'
    }
  }, true);
}

async function getGuid() {
  const extensionGuid = await getExtensionGuid();
  if (extensionGuid) return extensionGuid;
  const siteGuid = await getSiteGuid();
  if (siteGuid) return siteGuid;
  const serverGuid = await getServerGuid();
  if (serverGuid) return serverGuid;
  return false;
}
async function getServerGuid() {
  try {
    return await request({
      path: 'guid',
      data: {
        abt: 1
      }
    }).then(data => data.guid);
  } catch (err) {
    console.info(err);
  }
}
async function getExtensionGuid() {
  const guid = await getSetting('guid');
  return guid ? guid : false;
}
async function getSiteGuid() {
  const cookies = await chrome.cookies.get({
    url: 'https://getpocket.com/',
    name: 'sess_guid'
  });
  return cookies === null || cookies === void 0 ? void 0 : cookies.value;
}

/* On successful save
–––––––––––––––––––––––––––––––––––––––––––––––––– */

async function saveSuccess(tabId, payload) {
  // Update toolbar icon
  const {
    resolved_url,
    given_url,
    isLink
  } = payload; // fetch image and title from above

  const url = resolved_url || given_url; //eslint-disable-line

  if (!isLink) setToolbarIcon(tabId, true); // Get item preview

  getItemPreview(tabId, payload); // Get list of users tags for typeahead

  getStoredTags(tabId); // Premium: Request suggested tags

  getTagSuggestions(url, tabId);
}
/* Derive item preview from save response
–––––––––––––––––––––––––––––––––––––––––––––––––– */

async function getItemPreview(tabId, payload) {
  const item = await deriveItemData(payload);
  chrome.tabs.sendMessage(tabId, {
    action: UPDATE_ITEM_PREVIEW,
    payload: {
      item
    }
  });
}
/* Get stored tags
–––––––––––––––––––––––––––––––––––––––––––––––––– */


async function getStoredTags(tabId) {
  // Check for server tags
  const fetchedSince = (await getSetting('tags_fetched_timestamp')) || 0;
  const fetchTags = await fetchStoredTags(fetchedSince);
  const fetchedTags = fetchTags ? fetchTags.tags || [] : [];
  const tagsFromSettings = await getSetting('tags_stored');
  const parsedTags = tagsFromSettings ? JSON.parse(tagsFromSettings) : [];
  const tags_stored = [...new Set([].concat(...parsedTags, ...fetchedTags))];
  const tags = JSON.stringify(tags_stored);
  setSettings({
    tags_stored: tags,
    tags_fetched_timestamp: Date.now()
  });
  chrome.tabs.sendMessage(tabId, {
    action: UPDATE_STORED_TAGS,
    payload: {
      tags: tags_stored
    }
  });
}
/* Get suggested tags for premium users
–––––––––––––––––––––––––––––––––––––––––––––––––– */


async function getTagSuggestions(url, tabId) {
  const premiumStatus = await getSetting('premium_status');
  if (premiumStatus !== '1') return;

  try {
    const response = await getOnSaveTags(url);
    const suggestedTags = response ? response.suggested_tags.map(tag => tag.tag) : [];

    if (response) {
      chrome.tabs.sendMessage(tabId, {
        action: SUGGESTED_TAGS_SUCCESS,
        payload: {
          suggestedTags
        }
      });
    }
  } catch (err) {
    console.info(err === null || err === void 0 ? void 0 : err.xError);
  }
}

var extension_description$e = {
	message: "Die einfachste und schnellste Möglichkeit, Artikel, Videos und mehr zu speichern."
};
var heading_idle$e = {
	message: ""
};
var heading_error$e = {
	message: "Da ist etwas schiefgegangen."
};
var heading_saving$e = {
	message: "Speichern..."
};
var heading_saved$e = {
	message: "In Pocket gespeichert"
};
var heading_save_failed$e = {
	message: "Da ist etwas schiefgegangen."
};
var heading_removing$e = {
	message: "Wird entfernt ..."
};
var heading_removed$e = {
	message: "Entfernt"
};
var heading_remove_failed$e = {
	message: "Da ist etwas schiefgegangen."
};
var heading_tags_saving$e = {
	message: "Tags werden gespeichert …"
};
var heading_tags_saved$e = {
	message: "Tags gespeichert"
};
var heading_tags_failed$e = {
	message: "Da ist etwas schiefgegangen."
};
var heading_tags_error$e = {
	message: "Tags sind auf 25 Zeichen begrenzt."
};
var buttons_remove$e = {
	message: "Entfernen"
};
var buttons_mylist$e = {
	message: "Gespeichert"
};
var buttons_save$e = {
	message: "Speichern"
};
var context_menu_open_list$e = {
	message: "Öffne deine in Pocket Gespeichert"
};
var context_menu_discover_more$e = {
	message: "Entdecke noch mehr interessante Inhalte auf Pocket"
};
var context_menu_log_in$e = {
	message: "Einloggen"
};
var context_menu_log_out$e = {
	message: "Ausloggen"
};
var context_menu_save$e = {
	message: "In Pocket speichern"
};
var tagging_add_tags$e = {
	message: "Tags hinzufügen"
};
var options_header$e = {
	message: "Erweiterung zum Speichern in Pocket"
};
var options_login_title$e = {
	message: "Eingeloggt als"
};
var options_log_out$e = {
	message: "Ausloggen"
};
var options_log_in$e = {
	message: "Einloggen"
};
var options_shortcut_title$e = {
	message: "Tastenkombination"
};
var options_shortcut_record$e = {
	message: "Neue Tastenkombination festlegen"
};
var options_theme_title$e = {
	message: "Modus"
};
var options_theme_light$e = {
	message: "Hell"
};
var options_theme_dark$e = {
	message: "Dunkel"
};
var options_theme_system$e = {
	message: "Systemeinstellung verwenden"
};
var options_app_title$e = {
	message: "Die mobile Pocket-App"
};
var options_app_apple$e = {
	message: "Im Apple App Store herunterladen"
};
var options_app_google$e = {
	message: "In Google Play herunterladen"
};
var options_need_help$e = {
	message: "Du brauchst Hilfe?"
};
var options_email_us$e = {
	message: "Schreibe uns eine E-Mail"
};
var options_follow$e = {
	message: "Jetzt Pocket folgen"
};
var options_family$e = {
	message: "Pocket gehört zur Mozilla-Produktfamilie."
};
var options_privacy$e = {
	message: "Datenschutzrichtlinie"
};
var options_terms$e = {
	message: "AGB"
};
var de = {
	extension_description: extension_description$e,
	heading_idle: heading_idle$e,
	heading_error: heading_error$e,
	heading_saving: heading_saving$e,
	heading_saved: heading_saved$e,
	heading_save_failed: heading_save_failed$e,
	heading_removing: heading_removing$e,
	heading_removed: heading_removed$e,
	heading_remove_failed: heading_remove_failed$e,
	heading_tags_saving: heading_tags_saving$e,
	heading_tags_saved: heading_tags_saved$e,
	heading_tags_failed: heading_tags_failed$e,
	heading_tags_error: heading_tags_error$e,
	buttons_remove: buttons_remove$e,
	buttons_mylist: buttons_mylist$e,
	buttons_save: buttons_save$e,
	context_menu_open_list: context_menu_open_list$e,
	context_menu_discover_more: context_menu_discover_more$e,
	context_menu_log_in: context_menu_log_in$e,
	context_menu_log_out: context_menu_log_out$e,
	context_menu_save: context_menu_save$e,
	tagging_add_tags: tagging_add_tags$e,
	options_header: options_header$e,
	options_login_title: options_login_title$e,
	options_log_out: options_log_out$e,
	options_log_in: options_log_in$e,
	options_shortcut_title: options_shortcut_title$e,
	options_shortcut_record: options_shortcut_record$e,
	options_theme_title: options_theme_title$e,
	options_theme_light: options_theme_light$e,
	options_theme_dark: options_theme_dark$e,
	options_theme_system: options_theme_system$e,
	options_app_title: options_app_title$e,
	options_app_apple: options_app_apple$e,
	options_app_google: options_app_google$e,
	options_need_help: options_need_help$e,
	options_email_us: options_email_us$e,
	options_follow: options_follow$e,
	options_family: options_family$e,
	options_privacy: options_privacy$e,
	options_terms: options_terms$e
};

var extension_description$d = {
	message: "The easiest, fastest way to capture articles, videos, and more."
};
var heading_idle$d = {
	message: ""
};
var heading_error$d = {
	message: "Something went wrong!"
};
var heading_saving$d = {
	message: "Saving..."
};
var heading_saved$d = {
	message: "Saved to Pocket"
};
var heading_save_failed$d = {
	message: "Something went wrong!"
};
var heading_removing$d = {
	message: "Removing..."
};
var heading_removed$d = {
	message: "Removed"
};
var heading_remove_failed$d = {
	message: "Something went wrong!"
};
var heading_tags_saving$d = {
	message: "Saving tags..."
};
var heading_tags_saved$d = {
	message: "Tags saved"
};
var heading_tags_failed$d = {
	message: "Something went wrong!"
};
var heading_tags_error$d = {
	message: "Tags are limited to 25 characters"
};
var buttons_remove$d = {
	message: "Remove"
};
var buttons_mylist$d = {
	message: "Saves"
};
var buttons_save$d = {
	message: "Save"
};
var context_menu_open_list$d = {
	message: "Open Your Pocket Saves"
};
var context_menu_discover_more$d = {
	message: "Discover more at Pocket"
};
var context_menu_log_in$d = {
	message: "Log In"
};
var context_menu_log_out$d = {
	message: "Log Out"
};
var context_menu_save$d = {
	message: "Save To Pocket"
};
var tagging_add_tags$d = {
	message: "Add Tags"
};
var options_header$d = {
	message: "Save to Pocket extension"
};
var options_login_title$d = {
	message: "Logged in as"
};
var options_log_out$d = {
	message: "Log out"
};
var options_log_in$d = {
	message: "Log in"
};
var options_shortcut_title$d = {
	message: "Keyboard Shortcut"
};
var options_shortcut_record$d = {
	message: "Record a new shortcut"
};
var options_theme_title$d = {
	message: "Theme"
};
var options_theme_light$d = {
	message: "Light"
};
var options_theme_dark$d = {
	message: "Dark"
};
var options_theme_system$d = {
	message: "Use System Setting"
};
var options_app_title$d = {
	message: "Pocket’s Mobile App"
};
var options_app_apple$d = {
	message: "Download on the Apple App Store"
};
var options_app_google$d = {
	message: "Get it on Google Play"
};
var options_need_help$d = {
	message: "Need Help?"
};
var options_email_us$d = {
	message: "Email Us"
};
var options_follow$d = {
	message: "Follow Pocket"
};
var options_family$d = {
	message: "Pocket is part of the Mozilla family of products."
};
var options_privacy$d = {
	message: "Privacy policy"
};
var options_terms$d = {
	message: "Terms of service"
};
var en = {
	extension_description: extension_description$d,
	heading_idle: heading_idle$d,
	heading_error: heading_error$d,
	heading_saving: heading_saving$d,
	heading_saved: heading_saved$d,
	heading_save_failed: heading_save_failed$d,
	heading_removing: heading_removing$d,
	heading_removed: heading_removed$d,
	heading_remove_failed: heading_remove_failed$d,
	heading_tags_saving: heading_tags_saving$d,
	heading_tags_saved: heading_tags_saved$d,
	heading_tags_failed: heading_tags_failed$d,
	heading_tags_error: heading_tags_error$d,
	buttons_remove: buttons_remove$d,
	buttons_mylist: buttons_mylist$d,
	buttons_save: buttons_save$d,
	context_menu_open_list: context_menu_open_list$d,
	context_menu_discover_more: context_menu_discover_more$d,
	context_menu_log_in: context_menu_log_in$d,
	context_menu_log_out: context_menu_log_out$d,
	context_menu_save: context_menu_save$d,
	tagging_add_tags: tagging_add_tags$d,
	options_header: options_header$d,
	options_login_title: options_login_title$d,
	options_log_out: options_log_out$d,
	options_log_in: options_log_in$d,
	options_shortcut_title: options_shortcut_title$d,
	options_shortcut_record: options_shortcut_record$d,
	options_theme_title: options_theme_title$d,
	options_theme_light: options_theme_light$d,
	options_theme_dark: options_theme_dark$d,
	options_theme_system: options_theme_system$d,
	options_app_title: options_app_title$d,
	options_app_apple: options_app_apple$d,
	options_app_google: options_app_google$d,
	options_need_help: options_need_help$d,
	options_email_us: options_email_us$d,
	options_follow: options_follow$d,
	options_family: options_family$d,
	options_privacy: options_privacy$d,
	options_terms: options_terms$d
};

var extension_description$c = {
	message: "La forma más fácil y rápida de capturar artículos, vídeos y mucho más."
};
var heading_idle$c = {
	message: ""
};
var heading_error$c = {
	message: "¡Parece que algo ha ido mal!"
};
var heading_saving$c = {
	message: "Guardando…"
};
var heading_saved$c = {
	message: "Guardado en Pocket"
};
var heading_save_failed$c = {
	message: "¡Parece que algo ha ido mal!"
};
var heading_removing$c = {
	message: "Eliminando..."
};
var heading_removed$c = {
	message: "Eliminado"
};
var heading_remove_failed$c = {
	message: "¡Parece que algo ha ido mal!"
};
var heading_tags_saving$c = {
	message: "Guardando etiquetas..."
};
var heading_tags_saved$c = {
	message: "Etiquetas guardadas"
};
var heading_tags_failed$c = {
	message: "¡Parece que algo ha ido mal!"
};
var heading_tags_error$c = {
	message: "La longitud máxima de una etiqueta es 25 caracteres."
};
var buttons_remove$c = {
	message: "Eliminar"
};
var buttons_mylist$c = {
	message: "Guardados"
};
var buttons_save$c = {
	message: "Guardar"
};
var context_menu_open_list$c = {
	message: "Abrir tus artículos guardados en Pocket"
};
var context_menu_discover_more$c = {
	message: "Descubre más en Pocket"
};
var context_menu_log_in$c = {
	message: "Iniciar sesión"
};
var context_menu_log_out$c = {
	message: "Cerrar sesión"
};
var context_menu_save$c = {
	message: "Guardar en Pocket"
};
var tagging_add_tags$c = {
	message: "Añadir etiquetas"
};
var options_header$c = {
	message: "Extensión Guardar en Pocket"
};
var options_login_title$c = {
	message: "Has iniciado sesión como"
};
var options_log_out$c = {
	message: "Cerrar sesión"
};
var options_log_in$c = {
	message: "Iniciar sesión"
};
var options_shortcut_title$c = {
	message: "Atajo de teclado"
};
var options_shortcut_record$c = {
	message: "Grabar un nuevo atajo"
};
var options_theme_title$c = {
	message: "Tema"
};
var options_theme_light$c = {
	message: "Claro"
};
var options_theme_dark$c = {
	message: "Oscuro"
};
var options_theme_system$c = {
	message: "Usar configuración del sistema"
};
var options_app_title$c = {
	message: "Aplicación móvil de Pocket"
};
var options_app_apple$c = {
	message: "Descargar en la App Store de Apple"
};
var options_app_google$c = {
	message: "Consíguela en Google Play"
};
var options_need_help$c = {
	message: "¿Necesitas ayuda?"
};
var options_email_us$c = {
	message: "Envíanos un correo"
};
var options_follow$c = {
	message: "Seguir a Pocket"
};
var options_family$c = {
	message: "Pocket es parte de la familia de productos de Mozilla."
};
var options_privacy$c = {
	message: "Política de privacidad"
};
var options_terms$c = {
	message: "Condiciones de servicio"
};
var es = {
	extension_description: extension_description$c,
	heading_idle: heading_idle$c,
	heading_error: heading_error$c,
	heading_saving: heading_saving$c,
	heading_saved: heading_saved$c,
	heading_save_failed: heading_save_failed$c,
	heading_removing: heading_removing$c,
	heading_removed: heading_removed$c,
	heading_remove_failed: heading_remove_failed$c,
	heading_tags_saving: heading_tags_saving$c,
	heading_tags_saved: heading_tags_saved$c,
	heading_tags_failed: heading_tags_failed$c,
	heading_tags_error: heading_tags_error$c,
	buttons_remove: buttons_remove$c,
	buttons_mylist: buttons_mylist$c,
	buttons_save: buttons_save$c,
	context_menu_open_list: context_menu_open_list$c,
	context_menu_discover_more: context_menu_discover_more$c,
	context_menu_log_in: context_menu_log_in$c,
	context_menu_log_out: context_menu_log_out$c,
	context_menu_save: context_menu_save$c,
	tagging_add_tags: tagging_add_tags$c,
	options_header: options_header$c,
	options_login_title: options_login_title$c,
	options_log_out: options_log_out$c,
	options_log_in: options_log_in$c,
	options_shortcut_title: options_shortcut_title$c,
	options_shortcut_record: options_shortcut_record$c,
	options_theme_title: options_theme_title$c,
	options_theme_light: options_theme_light$c,
	options_theme_dark: options_theme_dark$c,
	options_theme_system: options_theme_system$c,
	options_app_title: options_app_title$c,
	options_app_apple: options_app_apple$c,
	options_app_google: options_app_google$c,
	options_need_help: options_need_help$c,
	options_email_us: options_email_us$c,
	options_follow: options_follow$c,
	options_family: options_family$c,
	options_privacy: options_privacy$c,
	options_terms: options_terms$c
};

var extension_description$b = {
	message: "La forma más fácil y rápida de capturar artículos, videos y más."
};
var heading_idle$b = {
	message: ""
};
var heading_error$b = {
	message: "¡Se produjo un error!"
};
var heading_saving$b = {
	message: "Guardando..."
};
var heading_saved$b = {
	message: "Guardado en Pocket"
};
var heading_save_failed$b = {
	message: "¡Se produjo un error!"
};
var heading_removing$b = {
	message: "Eliminando..."
};
var heading_removed$b = {
	message: "Eliminado"
};
var heading_remove_failed$b = {
	message: "¡Se produjo un error!"
};
var heading_tags_saving$b = {
	message: "Guardando etiquetas..."
};
var heading_tags_saved$b = {
	message: "Etiquetas guardadas"
};
var heading_tags_failed$b = {
	message: "¡Se produjo un error!"
};
var heading_tags_error$b = {
	message: "Las etiquetas se limitan a 25 caracteres"
};
var buttons_remove$b = {
	message: "Eliminar"
};
var buttons_mylist$b = {
	message: "Guardado"
};
var buttons_save$b = {
	message: "Guardar"
};
var context_menu_open_list$b = {
	message: "Abrir el contenido guardado en Pocket"
};
var context_menu_discover_more$b = {
	message: "Descubre más en Pocket"
};
var context_menu_log_in$b = {
	message: "Iniciar sesión"
};
var context_menu_log_out$b = {
	message: "Finalizar sesión"
};
var context_menu_save$b = {
	message: "Guardar en Pocket"
};
var tagging_add_tags$b = {
	message: "Agregar Etiquetas"
};
var options_header$b = {
	message: "Extensión para guardar en Pocket"
};
var options_login_title$b = {
	message: "Iniciaste sesión como"
};
var options_log_out$b = {
	message: "Cerrar sesión"
};
var options_log_in$b = {
	message: "Iniciar sesión"
};
var options_shortcut_title$b = {
	message: "Atajo de teclado"
};
var options_shortcut_record$b = {
	message: "Registra un nuevo atajo"
};
var options_theme_title$b = {
	message: "Tema"
};
var options_theme_light$b = {
	message: "Claro"
};
var options_theme_dark$b = {
	message: "Oscuro"
};
var options_theme_system$b = {
	message: "Usar configuración del sistema"
};
var options_app_title$b = {
	message: "Aplicación móvil de Pocket"
};
var options_app_apple$b = {
	message: "Descargar en el App Store de Apple"
};
var options_app_google$b = {
	message: "Obtenerlo en Google Play"
};
var options_need_help$b = {
	message: "¿Necesitas ayuda?"
};
var options_email_us$b = {
	message: "Envíanos un email"
};
var options_follow$b = {
	message: "Seguir a Pocket"
};
var options_family$b = {
	message: "Pocket forma parte de la familia de productos Mozilla."
};
var options_privacy$b = {
	message: "Política de privacidad"
};
var options_terms$b = {
	message: "Términos del Servicio"
};
var es_419 = {
	extension_description: extension_description$b,
	heading_idle: heading_idle$b,
	heading_error: heading_error$b,
	heading_saving: heading_saving$b,
	heading_saved: heading_saved$b,
	heading_save_failed: heading_save_failed$b,
	heading_removing: heading_removing$b,
	heading_removed: heading_removed$b,
	heading_remove_failed: heading_remove_failed$b,
	heading_tags_saving: heading_tags_saving$b,
	heading_tags_saved: heading_tags_saved$b,
	heading_tags_failed: heading_tags_failed$b,
	heading_tags_error: heading_tags_error$b,
	buttons_remove: buttons_remove$b,
	buttons_mylist: buttons_mylist$b,
	buttons_save: buttons_save$b,
	context_menu_open_list: context_menu_open_list$b,
	context_menu_discover_more: context_menu_discover_more$b,
	context_menu_log_in: context_menu_log_in$b,
	context_menu_log_out: context_menu_log_out$b,
	context_menu_save: context_menu_save$b,
	tagging_add_tags: tagging_add_tags$b,
	options_header: options_header$b,
	options_login_title: options_login_title$b,
	options_log_out: options_log_out$b,
	options_log_in: options_log_in$b,
	options_shortcut_title: options_shortcut_title$b,
	options_shortcut_record: options_shortcut_record$b,
	options_theme_title: options_theme_title$b,
	options_theme_light: options_theme_light$b,
	options_theme_dark: options_theme_dark$b,
	options_theme_system: options_theme_system$b,
	options_app_title: options_app_title$b,
	options_app_apple: options_app_apple$b,
	options_app_google: options_app_google$b,
	options_need_help: options_need_help$b,
	options_email_us: options_email_us$b,
	options_follow: options_follow$b,
	options_family: options_family$b,
	options_privacy: options_privacy$b,
	options_terms: options_terms$b
};

var extension_description$a = {
	message: "Le moyen le plus simple et le plus rapide de sauvegarder des articles, des vidéos et plus encore."
};
var heading_idle$a = {
	message: ""
};
var heading_error$a = {
	message: "Un problème est survenu !"
};
var heading_saving$a = {
	message: "Sauvegarde..."
};
var heading_saved$a = {
	message: "Sauvegardé dans Pocket"
};
var heading_save_failed$a = {
	message: "Un problème est survenu !"
};
var heading_removing$a = {
	message: "Suppression en cours..."
};
var heading_removed$a = {
	message: "Suppression effectuée"
};
var heading_remove_failed$a = {
	message: "Un problème est survenu !"
};
var heading_tags_saving$a = {
	message: "Sauvegarde des labels..."
};
var heading_tags_saved$a = {
	message: "Labels sauvegardés"
};
var heading_tags_failed$a = {
	message: "Un problème est survenu !"
};
var heading_tags_error$a = {
	message: "Les labels sont limités à 25 caractères"
};
var buttons_remove$a = {
	message: "Supprimer"
};
var buttons_mylist$a = {
	message: "Sauvegardes"
};
var buttons_save$a = {
	message: "Sauvegarder"
};
var context_menu_open_list$a = {
	message: "Ouvrez vos sauvegardes Pocket"
};
var context_menu_discover_more$a = {
	message: "Découvrez-en plus sur Pocket"
};
var context_menu_log_in$a = {
	message: "Se connecter"
};
var context_menu_log_out$a = {
	message: "Déconnexion"
};
var context_menu_save$a = {
	message: "Sauvegarder dans Pocket"
};
var tagging_add_tags$a = {
	message: "Ajouter des labels"
};
var options_header$a = {
	message: "Extension Sauvegarder dans Pocket"
};
var options_login_title$a = {
	message: "Connecté(e) en tant que"
};
var options_log_out$a = {
	message: "Déconnexion"
};
var options_log_in$a = {
	message: "Se connecter"
};
var options_shortcut_title$a = {
	message: "Raccourci clavier"
};
var options_shortcut_record$a = {
	message: "Enregistrer un nouveau raccourci"
};
var options_theme_title$a = {
	message: "Thème"
};
var options_theme_light$a = {
	message: "Clair"
};
var options_theme_dark$a = {
	message: "Foncé"
};
var options_theme_system$a = {
	message: "Utiliser le paramètre système"
};
var options_app_title$a = {
	message: "Application mobile de Pocket"
};
var options_app_apple$a = {
	message: "Télécharger sur l'Apple Store"
};
var options_app_google$a = {
	message: "Télécharger sur Google Play"
};
var options_need_help$a = {
	message: "Besoin d'aide ?"
};
var options_email_us$a = {
	message: "Nous écrire"
};
var options_follow$a = {
	message: "Suivez Pocket"
};
var options_family$a = {
	message: "Pocket fait partie de la famille de produits Mozilla."
};
var options_privacy$a = {
	message: "Politique de confidentialité"
};
var options_terms$a = {
	message: "Conditions générales d'utilisation"
};
var fr = {
	extension_description: extension_description$a,
	heading_idle: heading_idle$a,
	heading_error: heading_error$a,
	heading_saving: heading_saving$a,
	heading_saved: heading_saved$a,
	heading_save_failed: heading_save_failed$a,
	heading_removing: heading_removing$a,
	heading_removed: heading_removed$a,
	heading_remove_failed: heading_remove_failed$a,
	heading_tags_saving: heading_tags_saving$a,
	heading_tags_saved: heading_tags_saved$a,
	heading_tags_failed: heading_tags_failed$a,
	heading_tags_error: heading_tags_error$a,
	buttons_remove: buttons_remove$a,
	buttons_mylist: buttons_mylist$a,
	buttons_save: buttons_save$a,
	context_menu_open_list: context_menu_open_list$a,
	context_menu_discover_more: context_menu_discover_more$a,
	context_menu_log_in: context_menu_log_in$a,
	context_menu_log_out: context_menu_log_out$a,
	context_menu_save: context_menu_save$a,
	tagging_add_tags: tagging_add_tags$a,
	options_header: options_header$a,
	options_login_title: options_login_title$a,
	options_log_out: options_log_out$a,
	options_log_in: options_log_in$a,
	options_shortcut_title: options_shortcut_title$a,
	options_shortcut_record: options_shortcut_record$a,
	options_theme_title: options_theme_title$a,
	options_theme_light: options_theme_light$a,
	options_theme_dark: options_theme_dark$a,
	options_theme_system: options_theme_system$a,
	options_app_title: options_app_title$a,
	options_app_apple: options_app_apple$a,
	options_app_google: options_app_google$a,
	options_need_help: options_need_help$a,
	options_email_us: options_email_us$a,
	options_follow: options_follow$a,
	options_family: options_family$a,
	options_privacy: options_privacy$a,
	options_terms: options_terms$a
};

var extension_description$9 = {
	message: "Il modo più semplice e veloce per raccogliere articoli, video e molto altro."
};
var heading_idle$9 = {
	message: ""
};
var heading_error$9 = {
	message: "Qualcosa non ha funzionato."
};
var heading_saving$9 = {
	message: "Salvataggio..."
};
var heading_saved$9 = {
	message: "Salvato in Pocket"
};
var heading_save_failed$9 = {
	message: "Qualcosa non ha funzionato."
};
var heading_removing$9 = {
	message: "Rimozione in corso…"
};
var heading_removed$9 = {
	message: "Rimosso"
};
var heading_remove_failed$9 = {
	message: "Qualcosa non ha funzionato."
};
var heading_tags_saving$9 = {
	message: "Salvataggio tag in corso..."
};
var heading_tags_saved$9 = {
	message: "Tag salvati"
};
var heading_tags_failed$9 = {
	message: "Qualcosa non ha funzionato."
};
var heading_tags_error$9 = {
	message: "I tag hanno un limite di 25 caratteri"
};
var buttons_remove$9 = {
	message: "Elimina"
};
var buttons_mylist$9 = {
	message: "Salvati"
};
var buttons_save$9 = {
	message: "Salva"
};
var context_menu_open_list$9 = {
	message: "Apri i tuoi salvataggi Pocket"
};
var context_menu_discover_more$9 = {
	message: "Scopri di più con Pocket"
};
var context_menu_log_in$9 = {
	message: "Accedi"
};
var context_menu_log_out$9 = {
	message: "Esci"
};
var context_menu_save$9 = {
	message: "Salva in Pocket"
};
var tagging_add_tags$9 = {
	message: "Aggiungi tag"
};
var options_header$9 = {
	message: "Estensione Salva in Pocket"
};
var options_login_title$9 = {
	message: "Accesso eseguito come"
};
var options_log_out$9 = {
	message: "Esci"
};
var options_log_in$9 = {
	message: "Accedi"
};
var options_shortcut_title$9 = {
	message: "Scelta rapida da tastiera"
};
var options_shortcut_record$9 = {
	message: "Memorizza un nuovo tasto di scelta rapida"
};
var options_theme_title$9 = {
	message: "Tema"
};
var options_theme_light$9 = {
	message: "Chiaro"
};
var options_theme_dark$9 = {
	message: "Scuro"
};
var options_theme_system$9 = {
	message: "Usa impostazione di sistema"
};
var options_app_title$9 = {
	message: "App per dispositivi mobili Pocket"
};
var options_app_apple$9 = {
	message: "Scarica dall'App Store di Apple"
};
var options_app_google$9 = {
	message: "Scaricalo da Google Play"
};
var options_need_help$9 = {
	message: "Hai bisogno di aiuto?"
};
var options_email_us$9 = {
	message: "Scrivi un'email"
};
var options_follow$9 = {
	message: "Segui Pocket"
};
var options_family$9 = {
	message: "Pocket fa parte della famiglia di prodotti Mozilla."
};
var options_privacy$9 = {
	message: "Tutela della privacy"
};
var options_terms$9 = {
	message: "Condizioni d'uso"
};
var it = {
	extension_description: extension_description$9,
	heading_idle: heading_idle$9,
	heading_error: heading_error$9,
	heading_saving: heading_saving$9,
	heading_saved: heading_saved$9,
	heading_save_failed: heading_save_failed$9,
	heading_removing: heading_removing$9,
	heading_removed: heading_removed$9,
	heading_remove_failed: heading_remove_failed$9,
	heading_tags_saving: heading_tags_saving$9,
	heading_tags_saved: heading_tags_saved$9,
	heading_tags_failed: heading_tags_failed$9,
	heading_tags_error: heading_tags_error$9,
	buttons_remove: buttons_remove$9,
	buttons_mylist: buttons_mylist$9,
	buttons_save: buttons_save$9,
	context_menu_open_list: context_menu_open_list$9,
	context_menu_discover_more: context_menu_discover_more$9,
	context_menu_log_in: context_menu_log_in$9,
	context_menu_log_out: context_menu_log_out$9,
	context_menu_save: context_menu_save$9,
	tagging_add_tags: tagging_add_tags$9,
	options_header: options_header$9,
	options_login_title: options_login_title$9,
	options_log_out: options_log_out$9,
	options_log_in: options_log_in$9,
	options_shortcut_title: options_shortcut_title$9,
	options_shortcut_record: options_shortcut_record$9,
	options_theme_title: options_theme_title$9,
	options_theme_light: options_theme_light$9,
	options_theme_dark: options_theme_dark$9,
	options_theme_system: options_theme_system$9,
	options_app_title: options_app_title$9,
	options_app_apple: options_app_apple$9,
	options_app_google: options_app_google$9,
	options_need_help: options_need_help$9,
	options_email_us: options_email_us$9,
	options_follow: options_follow$9,
	options_family: options_family$9,
	options_privacy: options_privacy$9,
	options_terms: options_terms$9
};

var extension_description$8 = {
	message: "記事、ビデオなどを最も簡単かつ迅速に取り込むことができます。"
};
var heading_idle$8 = {
	message: ""
};
var heading_error$8 = {
	message: "エラーが発生したようです。"
};
var heading_saving$8 = {
	message: "保存中..."
};
var heading_saved$8 = {
	message: "Pocket に保存済み"
};
var heading_save_failed$8 = {
	message: "エラーが発生したようです。"
};
var heading_removing$8 = {
	message: "削除しています..."
};
var heading_removed$8 = {
	message: "削除されました"
};
var heading_remove_failed$8 = {
	message: "エラーが発生したようです。"
};
var heading_tags_saving$8 = {
	message: "タグを保存しています..."
};
var heading_tags_saved$8 = {
	message: "タグが保存されました"
};
var heading_tags_failed$8 = {
	message: "エラーが発生したようです。"
};
var heading_tags_error$8 = {
	message: "タグは最大25文字となっています"
};
var buttons_remove$8 = {
	message: "削除"
};
var buttons_mylist$8 = {
	message: "保存アイテム"
};
var buttons_save$8 = {
	message: "保存"
};
var context_menu_open_list$8 = {
	message: "Pocket の保存アイテムを開く"
};
var context_menu_discover_more$8 = {
	message: "Pocket で他のコンテンツを発見"
};
var context_menu_log_in$8 = {
	message: "ログイン"
};
var context_menu_log_out$8 = {
	message: "ログアウト"
};
var context_menu_save$8 = {
	message: "Pocket に保存"
};
var tagging_add_tags$8 = {
	message: "タグを追加"
};
var options_header$8 = {
	message: "「Pocket に保存」拡張機能"
};
var options_login_title$8 = {
	message: "次のユーザー名でログイン中："
};
var options_log_out$8 = {
	message: "ログアウト"
};
var options_log_in$8 = {
	message: "ログイン"
};
var options_shortcut_title$8 = {
	message: "キーボードショートカット"
};
var options_shortcut_record$8 = {
	message: "新しいショートカットを記録"
};
var options_theme_title$8 = {
	message: "テーマ"
};
var options_theme_light$8 = {
	message: "ライト"
};
var options_theme_dark$8 = {
	message: "ダーク"
};
var options_theme_system$8 = {
	message: "システム設定を使用する"
};
var options_app_title$8 = {
	message: "Pocket モバイルアプリ"
};
var options_app_apple$8 = {
	message: "Apple App Store でダウンロード"
};
var options_app_google$8 = {
	message: "Google Playからダウンロード"
};
var options_need_help$8 = {
	message: "お困りですか？"
};
var options_email_us$8 = {
	message: "メールでお問い合わせ"
};
var options_follow$8 = {
	message: "Pocket をフォロー"
};
var options_family$8 = {
	message: "Pocket は Mozilla 製品ファミリーの一部です。"
};
var options_privacy$8 = {
	message: "プライバシーポリシー"
};
var options_terms$8 = {
	message: "サービス利用規約"
};
var ja = {
	extension_description: extension_description$8,
	heading_idle: heading_idle$8,
	heading_error: heading_error$8,
	heading_saving: heading_saving$8,
	heading_saved: heading_saved$8,
	heading_save_failed: heading_save_failed$8,
	heading_removing: heading_removing$8,
	heading_removed: heading_removed$8,
	heading_remove_failed: heading_remove_failed$8,
	heading_tags_saving: heading_tags_saving$8,
	heading_tags_saved: heading_tags_saved$8,
	heading_tags_failed: heading_tags_failed$8,
	heading_tags_error: heading_tags_error$8,
	buttons_remove: buttons_remove$8,
	buttons_mylist: buttons_mylist$8,
	buttons_save: buttons_save$8,
	context_menu_open_list: context_menu_open_list$8,
	context_menu_discover_more: context_menu_discover_more$8,
	context_menu_log_in: context_menu_log_in$8,
	context_menu_log_out: context_menu_log_out$8,
	context_menu_save: context_menu_save$8,
	tagging_add_tags: tagging_add_tags$8,
	options_header: options_header$8,
	options_login_title: options_login_title$8,
	options_log_out: options_log_out$8,
	options_log_in: options_log_in$8,
	options_shortcut_title: options_shortcut_title$8,
	options_shortcut_record: options_shortcut_record$8,
	options_theme_title: options_theme_title$8,
	options_theme_light: options_theme_light$8,
	options_theme_dark: options_theme_dark$8,
	options_theme_system: options_theme_system$8,
	options_app_title: options_app_title$8,
	options_app_apple: options_app_apple$8,
	options_app_google: options_app_google$8,
	options_need_help: options_need_help$8,
	options_email_us: options_email_us$8,
	options_follow: options_follow$8,
	options_family: options_family$8,
	options_privacy: options_privacy$8,
	options_terms: options_terms$8
};

var extension_description$7 = {
	message: "아티클, 동영상 등을 캡처하는 가장 쉽고 빠른 방법."
};
var heading_idle$7 = {
	message: ""
};
var heading_error$7 = {
	message: "문제가 발생했습니다!"
};
var heading_saving$7 = {
	message: "저장 중..."
};
var heading_saved$7 = {
	message: "Pocket에 저장됨"
};
var heading_save_failed$7 = {
	message: "문제가 발생했습니다!"
};
var heading_removing$7 = {
	message: "제거 중..."
};
var heading_removed$7 = {
	message: "제거됨"
};
var heading_remove_failed$7 = {
	message: "문제가 발생했습니다!"
};
var heading_tags_saving$7 = {
	message: "태그 저장 중..."
};
var heading_tags_saved$7 = {
	message: "태그 저장됨"
};
var heading_tags_failed$7 = {
	message: "문제가 발생했습니다!"
};
var heading_tags_error$7 = {
	message: "태그는 25자로 제한됩니다."
};
var buttons_remove$7 = {
	message: "제거하기"
};
var buttons_mylist$7 = {
	message: "저장"
};
var buttons_save$7 = {
	message: "저장"
};
var context_menu_open_list$7 = {
	message: "Pocket Saves 열기"
};
var context_menu_discover_more$7 = {
	message: "Pocket에서 더 찾기"
};
var context_menu_log_in$7 = {
	message: "로그인"
};
var context_menu_log_out$7 = {
	message: "로그아웃"
};
var context_menu_save$7 = {
	message: "Pocket에 저장"
};
var tagging_add_tags$7 = {
	message: "태그 추가"
};
var options_header$7 = {
	message: "Pocket 확장에 저장"
};
var options_login_title$7 = {
	message: "다음 이름으로 로그인됨"
};
var options_log_out$7 = {
	message: "로그아웃"
};
var options_log_in$7 = {
	message: "로그인"
};
var options_shortcut_title$7 = {
	message: "키보드 바로 가기"
};
var options_shortcut_record$7 = {
	message: "새 바로 가기 기록"
};
var options_theme_title$7 = {
	message: "테마"
};
var options_theme_light$7 = {
	message: "밝게"
};
var options_theme_dark$7 = {
	message: "어둡게"
};
var options_theme_system$7 = {
	message: "시스템 설정 사용"
};
var options_app_title$7 = {
	message: "Pocket 모바일 앱"
};
var options_app_apple$7 = {
	message: "Apple App Store에서 다운로드"
};
var options_app_google$7 = {
	message: "Google Play에서 다운로드"
};
var options_need_help$7 = {
	message: "도움이 필요하십니까?"
};
var options_email_us$7 = {
	message: "이메일 보내기"
};
var options_follow$7 = {
	message: "Pocket 팔로우"
};
var options_family$7 = {
	message: "Pocket은 Mozilla 제품군의 일부입니다."
};
var options_privacy$7 = {
	message: "개인정보 보호정책"
};
var options_terms$7 = {
	message: "서비스 약관"
};
var ko = {
	extension_description: extension_description$7,
	heading_idle: heading_idle$7,
	heading_error: heading_error$7,
	heading_saving: heading_saving$7,
	heading_saved: heading_saved$7,
	heading_save_failed: heading_save_failed$7,
	heading_removing: heading_removing$7,
	heading_removed: heading_removed$7,
	heading_remove_failed: heading_remove_failed$7,
	heading_tags_saving: heading_tags_saving$7,
	heading_tags_saved: heading_tags_saved$7,
	heading_tags_failed: heading_tags_failed$7,
	heading_tags_error: heading_tags_error$7,
	buttons_remove: buttons_remove$7,
	buttons_mylist: buttons_mylist$7,
	buttons_save: buttons_save$7,
	context_menu_open_list: context_menu_open_list$7,
	context_menu_discover_more: context_menu_discover_more$7,
	context_menu_log_in: context_menu_log_in$7,
	context_menu_log_out: context_menu_log_out$7,
	context_menu_save: context_menu_save$7,
	tagging_add_tags: tagging_add_tags$7,
	options_header: options_header$7,
	options_login_title: options_login_title$7,
	options_log_out: options_log_out$7,
	options_log_in: options_log_in$7,
	options_shortcut_title: options_shortcut_title$7,
	options_shortcut_record: options_shortcut_record$7,
	options_theme_title: options_theme_title$7,
	options_theme_light: options_theme_light$7,
	options_theme_dark: options_theme_dark$7,
	options_theme_system: options_theme_system$7,
	options_app_title: options_app_title$7,
	options_app_apple: options_app_apple$7,
	options_app_google: options_app_google$7,
	options_need_help: options_need_help$7,
	options_email_us: options_email_us$7,
	options_follow: options_follow$7,
	options_family: options_family$7,
	options_privacy: options_privacy$7,
	options_terms: options_terms$7
};

var extension_description$6 = {
	message: "De gemakkelijkste en snelste manier om artikelen, video's en meer op te slaan."
};
var heading_idle$6 = {
	message: ""
};
var heading_error$6 = {
	message: "Er is iets misgegaan!"
};
var heading_saving$6 = {
	message: "Opslaan..."
};
var heading_saved$6 = {
	message: "Opgeslagen naar Pocket"
};
var heading_save_failed$6 = {
	message: "Er is iets misgegaan!"
};
var heading_removing$6 = {
	message: "Verwijderen..."
};
var heading_removed$6 = {
	message: "Verwijderd"
};
var heading_remove_failed$6 = {
	message: "Er is iets misgegaan!"
};
var heading_tags_saving$6 = {
	message: "Tags opslaan..."
};
var heading_tags_saved$6 = {
	message: "Tags opgeslagen"
};
var heading_tags_failed$6 = {
	message: "Er is iets misgegaan!"
};
var heading_tags_error$6 = {
	message: "Tags zijn beperkt tot 25 tekens"
};
var buttons_remove$6 = {
	message: "Verwijderen"
};
var buttons_mylist$6 = {
	message: "Opgeslagen"
};
var buttons_save$6 = {
	message: "Opslaan"
};
var context_menu_open_list$6 = {
	message: "Open Opgeslagen in Pocket"
};
var context_menu_discover_more$6 = {
	message: "Ontdek meer op Pocket"
};
var context_menu_log_in$6 = {
	message: "Inloggen"
};
var context_menu_log_out$6 = {
	message: "Uitloggen"
};
var context_menu_save$6 = {
	message: "Opslaan naar Pocket"
};
var tagging_add_tags$6 = {
	message: "Tags toevoegen"
};
var options_header$6 = {
	message: "Extensie Naar Pocket opslaan"
};
var options_login_title$6 = {
	message: "Ingelogd als"
};
var options_log_out$6 = {
	message: "Afmelden"
};
var options_log_in$6 = {
	message: "Inloggen"
};
var options_shortcut_title$6 = {
	message: "Sneltoets"
};
var options_shortcut_record$6 = {
	message: "Een nieuwe snelkoppeling vastleggen"
};
var options_theme_title$6 = {
	message: "Thema"
};
var options_theme_light$6 = {
	message: "Licht"
};
var options_theme_dark$6 = {
	message: "Donker"
};
var options_theme_system$6 = {
	message: "Systeeminstelling gebruiken"
};
var options_app_title$6 = {
	message: "Mobiele Pocket-app"
};
var options_app_apple$6 = {
	message: "Downloaden in de appstore van Apple"
};
var options_app_google$6 = {
	message: "Downloaden via Google Play"
};
var options_need_help$6 = {
	message: "Hulp nodig?"
};
var options_email_us$6 = {
	message: "Mail ons"
};
var options_follow$6 = {
	message: "Volg Pocket"
};
var options_family$6 = {
	message: "Pocket maakt deel uit van de Mozilla-productfamilie."
};
var options_privacy$6 = {
	message: "Privacybeleid"
};
var options_terms$6 = {
	message: "Gebruiksvoorwaarden"
};
var nl = {
	extension_description: extension_description$6,
	heading_idle: heading_idle$6,
	heading_error: heading_error$6,
	heading_saving: heading_saving$6,
	heading_saved: heading_saved$6,
	heading_save_failed: heading_save_failed$6,
	heading_removing: heading_removing$6,
	heading_removed: heading_removed$6,
	heading_remove_failed: heading_remove_failed$6,
	heading_tags_saving: heading_tags_saving$6,
	heading_tags_saved: heading_tags_saved$6,
	heading_tags_failed: heading_tags_failed$6,
	heading_tags_error: heading_tags_error$6,
	buttons_remove: buttons_remove$6,
	buttons_mylist: buttons_mylist$6,
	buttons_save: buttons_save$6,
	context_menu_open_list: context_menu_open_list$6,
	context_menu_discover_more: context_menu_discover_more$6,
	context_menu_log_in: context_menu_log_in$6,
	context_menu_log_out: context_menu_log_out$6,
	context_menu_save: context_menu_save$6,
	tagging_add_tags: tagging_add_tags$6,
	options_header: options_header$6,
	options_login_title: options_login_title$6,
	options_log_out: options_log_out$6,
	options_log_in: options_log_in$6,
	options_shortcut_title: options_shortcut_title$6,
	options_shortcut_record: options_shortcut_record$6,
	options_theme_title: options_theme_title$6,
	options_theme_light: options_theme_light$6,
	options_theme_dark: options_theme_dark$6,
	options_theme_system: options_theme_system$6,
	options_app_title: options_app_title$6,
	options_app_apple: options_app_apple$6,
	options_app_google: options_app_google$6,
	options_need_help: options_need_help$6,
	options_email_us: options_email_us$6,
	options_follow: options_follow$6,
	options_family: options_family$6,
	options_privacy: options_privacy$6,
	options_terms: options_terms$6
};

var extension_description$5 = {
	message: "Najłatwiejsza i najszybsza metoda zapisywania artykułów, filmów i innych treści."
};
var heading_idle$5 = {
	message: ""
};
var heading_error$5 = {
	message: "Wystąpił problem."
};
var heading_saving$5 = {
	message: "Zapisywanie..."
};
var heading_saved$5 = {
	message: "Zapisano w aplikacji Pocket"
};
var heading_save_failed$5 = {
	message: "Wystąpił problem."
};
var heading_removing$5 = {
	message: "Usuwanie..."
};
var heading_removed$5 = {
	message: "Usunięto"
};
var heading_remove_failed$5 = {
	message: "Wystąpił problem."
};
var heading_tags_saving$5 = {
	message: "Zapisywanie tagów..."
};
var heading_tags_saved$5 = {
	message: "Zapisano tagi"
};
var heading_tags_failed$5 = {
	message: "Wystąpił problem."
};
var heading_tags_error$5 = {
	message: "Tagi mogą mieć maksymalnie 25 znaków"
};
var buttons_remove$5 = {
	message: "Usuń"
};
var buttons_mylist$5 = {
	message: "Zapisane"
};
var buttons_save$5 = {
	message: "Zapisz"
};
var context_menu_open_list$5 = {
	message: "Otwórz elementy zapisane w Pocket"
};
var context_menu_discover_more$5 = {
	message: "Odkryj więcej w Pocket"
};
var context_menu_log_in$5 = {
	message: "Zaloguj się"
};
var context_menu_log_out$5 = {
	message: "Wyloguj się"
};
var context_menu_save$5 = {
	message: "Zapisz w aplikacji Pocket"
};
var tagging_add_tags$5 = {
	message: "Dodaj tagi"
};
var options_header$5 = {
	message: "Rozszerzenie Zapisz do Pocket"
};
var options_login_title$5 = {
	message: "Zalogowano jako"
};
var options_log_out$5 = {
	message: "Wyloguj się"
};
var options_log_in$5 = {
	message: "Zaloguj się"
};
var options_shortcut_title$5 = {
	message: "Skrót klawiaturowy"
};
var options_shortcut_record$5 = {
	message: "Zarejestruj nowy skrót"
};
var options_theme_title$5 = {
	message: "Motyw"
};
var options_theme_light$5 = {
	message: "Jasny"
};
var options_theme_dark$5 = {
	message: "Ciemny"
};
var options_theme_system$5 = {
	message: "Użyj ustawienia systemowego"
};
var options_app_title$5 = {
	message: "Aplikacja mobilna Pocket"
};
var options_app_apple$5 = {
	message: "Pobierz z serwisu Apple App Store"
};
var options_app_google$5 = {
	message: "Pobierz z serwisu Google Play"
};
var options_need_help$5 = {
	message: "Potrzebna pomoc?"
};
var options_email_us$5 = {
	message: "Napisz do nas wiadomość e-mail"
};
var options_follow$5 = {
	message: "Obserwuj Pocket"
};
var options_family$5 = {
	message: "Pocket należy do rodziny produktów Mozilla."
};
var options_privacy$5 = {
	message: "Zasady ochrony prywatności"
};
var options_terms$5 = {
	message: "Warunki użytkowania usługi"
};
var pl = {
	extension_description: extension_description$5,
	heading_idle: heading_idle$5,
	heading_error: heading_error$5,
	heading_saving: heading_saving$5,
	heading_saved: heading_saved$5,
	heading_save_failed: heading_save_failed$5,
	heading_removing: heading_removing$5,
	heading_removed: heading_removed$5,
	heading_remove_failed: heading_remove_failed$5,
	heading_tags_saving: heading_tags_saving$5,
	heading_tags_saved: heading_tags_saved$5,
	heading_tags_failed: heading_tags_failed$5,
	heading_tags_error: heading_tags_error$5,
	buttons_remove: buttons_remove$5,
	buttons_mylist: buttons_mylist$5,
	buttons_save: buttons_save$5,
	context_menu_open_list: context_menu_open_list$5,
	context_menu_discover_more: context_menu_discover_more$5,
	context_menu_log_in: context_menu_log_in$5,
	context_menu_log_out: context_menu_log_out$5,
	context_menu_save: context_menu_save$5,
	tagging_add_tags: tagging_add_tags$5,
	options_header: options_header$5,
	options_login_title: options_login_title$5,
	options_log_out: options_log_out$5,
	options_log_in: options_log_in$5,
	options_shortcut_title: options_shortcut_title$5,
	options_shortcut_record: options_shortcut_record$5,
	options_theme_title: options_theme_title$5,
	options_theme_light: options_theme_light$5,
	options_theme_dark: options_theme_dark$5,
	options_theme_system: options_theme_system$5,
	options_app_title: options_app_title$5,
	options_app_apple: options_app_apple$5,
	options_app_google: options_app_google$5,
	options_need_help: options_need_help$5,
	options_email_us: options_email_us$5,
	options_follow: options_follow$5,
	options_family: options_family$5,
	options_privacy: options_privacy$5,
	options_terms: options_terms$5
};

var extension_description$4 = {
	message: "A maneira mais fácil e rápida de salvar artigos, vídeos e muito mais."
};
var heading_idle$4 = {
	message: ""
};
var heading_error$4 = {
	message: "Ocorreu um erro!"
};
var heading_saving$4 = {
	message: "Salvando…"
};
var heading_saved$4 = {
	message: "Salvo no Pocket"
};
var heading_save_failed$4 = {
	message: "Ocorreu um erro!"
};
var heading_removing$4 = {
	message: "Removendo..."
};
var heading_removed$4 = {
	message: "Removido"
};
var heading_remove_failed$4 = {
	message: "Ocorreu um erro!"
};
var heading_tags_saving$4 = {
	message: "Salvando tags..."
};
var heading_tags_saved$4 = {
	message: "Tags salvas"
};
var heading_tags_failed$4 = {
	message: "Ocorreu um erro!"
};
var heading_tags_error$4 = {
	message: "As tags têm um limite de 25 caracteres"
};
var buttons_remove$4 = {
	message: "Remover"
};
var buttons_mylist$4 = {
	message: "Salvos"
};
var buttons_save$4 = {
	message: "Salvar"
};
var context_menu_open_list$4 = {
	message: "Abra seus Salvos no Pocket"
};
var context_menu_discover_more$4 = {
	message: "Descubra mais no Pocket"
};
var context_menu_log_in$4 = {
	message: "Entrar"
};
var context_menu_log_out$4 = {
	message: "Sair"
};
var context_menu_save$4 = {
	message: "Salvar no Pocket"
};
var tagging_add_tags$4 = {
	message: "Adicionar tags"
};
var options_header$4 = {
	message: "Extensão Salvar no Pocket"
};
var options_login_title$4 = {
	message: "Conectado como"
};
var options_log_out$4 = {
	message: "Sair"
};
var options_log_in$4 = {
	message: "Entrar"
};
var options_shortcut_title$4 = {
	message: "Atalho do teclado"
};
var options_shortcut_record$4 = {
	message: "Gravar um novo atalho"
};
var options_theme_title$4 = {
	message: "Tema"
};
var options_theme_light$4 = {
	message: "Claro"
};
var options_theme_dark$4 = {
	message: "Escuro"
};
var options_theme_system$4 = {
	message: "Usar a configuração do sistema"
};
var options_app_title$4 = {
	message: "Aplicativo móvel do Pocket"
};
var options_app_apple$4 = {
	message: "Baixe o aplicativo na App Store da Apple"
};
var options_app_google$4 = {
	message: "Baixar no Google Play"
};
var options_need_help$4 = {
	message: "Precisa de ajuda?"
};
var options_email_us$4 = {
	message: "Envie-nos um e-mail"
};
var options_follow$4 = {
	message: "Siga o Pocket"
};
var options_family$4 = {
	message: "O Pocket faz parte da linha de produtos da Mozilla."
};
var options_privacy$4 = {
	message: "Política de privacidade"
};
var options_terms$4 = {
	message: "Termos de serviço"
};
var pt_BR = {
	extension_description: extension_description$4,
	heading_idle: heading_idle$4,
	heading_error: heading_error$4,
	heading_saving: heading_saving$4,
	heading_saved: heading_saved$4,
	heading_save_failed: heading_save_failed$4,
	heading_removing: heading_removing$4,
	heading_removed: heading_removed$4,
	heading_remove_failed: heading_remove_failed$4,
	heading_tags_saving: heading_tags_saving$4,
	heading_tags_saved: heading_tags_saved$4,
	heading_tags_failed: heading_tags_failed$4,
	heading_tags_error: heading_tags_error$4,
	buttons_remove: buttons_remove$4,
	buttons_mylist: buttons_mylist$4,
	buttons_save: buttons_save$4,
	context_menu_open_list: context_menu_open_list$4,
	context_menu_discover_more: context_menu_discover_more$4,
	context_menu_log_in: context_menu_log_in$4,
	context_menu_log_out: context_menu_log_out$4,
	context_menu_save: context_menu_save$4,
	tagging_add_tags: tagging_add_tags$4,
	options_header: options_header$4,
	options_login_title: options_login_title$4,
	options_log_out: options_log_out$4,
	options_log_in: options_log_in$4,
	options_shortcut_title: options_shortcut_title$4,
	options_shortcut_record: options_shortcut_record$4,
	options_theme_title: options_theme_title$4,
	options_theme_light: options_theme_light$4,
	options_theme_dark: options_theme_dark$4,
	options_theme_system: options_theme_system$4,
	options_app_title: options_app_title$4,
	options_app_apple: options_app_apple$4,
	options_app_google: options_app_google$4,
	options_need_help: options_need_help$4,
	options_email_us: options_email_us$4,
	options_follow: options_follow$4,
	options_family: options_family$4,
	options_privacy: options_privacy$4,
	options_terms: options_terms$4
};

var extension_description$3 = {
	message: "A maneira mais fácil e rápida de capturar artigos, vídeos e muito mais."
};
var heading_idle$3 = {
	message: ""
};
var heading_error$3 = {
	message: "Algo correu mal!"
};
var heading_saving$3 = {
	message: "A guardar…"
};
var heading_saved$3 = {
	message: "Guardado no Pocket"
};
var heading_save_failed$3 = {
	message: "Algo correu mal!"
};
var heading_removing$3 = {
	message: "A remover..."
};
var heading_removed$3 = {
	message: "Removido"
};
var heading_remove_failed$3 = {
	message: "Algo correu mal!"
};
var heading_tags_saving$3 = {
	message: "A guardar etiquetas..."
};
var heading_tags_saved$3 = {
	message: "Etiquetas guardadas"
};
var heading_tags_failed$3 = {
	message: "Algo correu mal!"
};
var heading_tags_error$3 = {
	message: "As etiquetas têm um limite de 25 caracteres"
};
var buttons_remove$3 = {
	message: "Remover"
};
var buttons_mylist$3 = {
	message: "Guardados"
};
var buttons_save$3 = {
	message: "Guardar"
};
var context_menu_open_list$3 = {
	message: "Abra os seus Guardados no Pocket"
};
var context_menu_discover_more$3 = {
	message: "Descubra mais no Pocket"
};
var context_menu_log_in$3 = {
	message: "Entrar"
};
var context_menu_log_out$3 = {
	message: "Sair"
};
var context_menu_save$3 = {
	message: "Guardar no Pocket"
};
var tagging_add_tags$3 = {
	message: "Adicionar Etiquetas"
};
var options_header$3 = {
	message: "Guardar na extensão do Pocket"
};
var options_login_title$3 = {
	message: "Sessão iniciada como"
};
var options_log_out$3 = {
	message: "Terminar sessão"
};
var options_log_in$3 = {
	message: "Iniciar sessão"
};
var options_shortcut_title$3 = {
	message: "Atalhos de teclado"
};
var options_shortcut_record$3 = {
	message: "Gravar um atalho novo"
};
var options_theme_title$3 = {
	message: "Tema"
};
var options_theme_light$3 = {
	message: "Claro"
};
var options_theme_dark$3 = {
	message: "Escuro"
};
var options_theme_system$3 = {
	message: "Usar a definição do sistema"
};
var options_app_title$3 = {
	message: "Aplicação móvel do Pocket"
};
var options_app_apple$3 = {
	message: "Transferir na Apple App Store"
};
var options_app_google$3 = {
	message: "Obtenha a app no Google Play"
};
var options_need_help$3 = {
	message: "Precisa de Ajuda?"
};
var options_email_us$3 = {
	message: "Envie-nos um e-mail"
};
var options_follow$3 = {
	message: "Seguir o Pocket"
};
var options_family$3 = {
	message: "O Pocket faz parte da família de produtos Mozilla."
};
var options_privacy$3 = {
	message: "Política de privacidade"
};
var options_terms$3 = {
	message: "Condições do serviço"
};
var pt_PT = {
	extension_description: extension_description$3,
	heading_idle: heading_idle$3,
	heading_error: heading_error$3,
	heading_saving: heading_saving$3,
	heading_saved: heading_saved$3,
	heading_save_failed: heading_save_failed$3,
	heading_removing: heading_removing$3,
	heading_removed: heading_removed$3,
	heading_remove_failed: heading_remove_failed$3,
	heading_tags_saving: heading_tags_saving$3,
	heading_tags_saved: heading_tags_saved$3,
	heading_tags_failed: heading_tags_failed$3,
	heading_tags_error: heading_tags_error$3,
	buttons_remove: buttons_remove$3,
	buttons_mylist: buttons_mylist$3,
	buttons_save: buttons_save$3,
	context_menu_open_list: context_menu_open_list$3,
	context_menu_discover_more: context_menu_discover_more$3,
	context_menu_log_in: context_menu_log_in$3,
	context_menu_log_out: context_menu_log_out$3,
	context_menu_save: context_menu_save$3,
	tagging_add_tags: tagging_add_tags$3,
	options_header: options_header$3,
	options_login_title: options_login_title$3,
	options_log_out: options_log_out$3,
	options_log_in: options_log_in$3,
	options_shortcut_title: options_shortcut_title$3,
	options_shortcut_record: options_shortcut_record$3,
	options_theme_title: options_theme_title$3,
	options_theme_light: options_theme_light$3,
	options_theme_dark: options_theme_dark$3,
	options_theme_system: options_theme_system$3,
	options_app_title: options_app_title$3,
	options_app_apple: options_app_apple$3,
	options_app_google: options_app_google$3,
	options_need_help: options_need_help$3,
	options_email_us: options_email_us$3,
	options_follow: options_follow$3,
	options_family: options_family$3,
	options_privacy: options_privacy$3,
	options_terms: options_terms$3
};

var extension_description$2 = {
	message: "Самый простой и быстрый способ записывать статьи, видео и многое другое."
};
var heading_idle$2 = {
	message: ""
};
var heading_error$2 = {
	message: "К сожалению, что-то пошло не так!"
};
var heading_saving$2 = {
	message: "Сохранение..."
};
var heading_saved$2 = {
	message: "Сохранено в Pocket"
};
var heading_save_failed$2 = {
	message: "К сожалению, что-то пошло не так!"
};
var heading_removing$2 = {
	message: "Удаление..."
};
var heading_removed$2 = {
	message: "Удалено"
};
var heading_remove_failed$2 = {
	message: "К сожалению, что-то пошло не так!"
};
var heading_tags_saving$2 = {
	message: "Сохранение тегов..."
};
var heading_tags_saved$2 = {
	message: "Теги сохранены"
};
var heading_tags_failed$2 = {
	message: "К сожалению, что-то пошло не так!"
};
var heading_tags_error$2 = {
	message: "Длина тега ограничена 25 символами"
};
var buttons_remove$2 = {
	message: "Удалить"
};
var buttons_mylist$2 = {
	message: "Сохраненное"
};
var buttons_save$2 = {
	message: "Сохранить"
};
var context_menu_open_list$2 = {
	message: "Откройте сохраненные файлы Pocket"
};
var context_menu_discover_more$2 = {
	message: "Откройте больше с Pocket"
};
var context_menu_log_in$2 = {
	message: "Вход"
};
var context_menu_log_out$2 = {
	message: "Выйти"
};
var context_menu_save$2 = {
	message: "Сохранить в Pocket"
};
var tagging_add_tags$2 = {
	message: "Добавить теги"
};
var options_header$2 = {
	message: "Расширение \"Сохранить в Pocket\""
};
var options_login_title$2 = {
	message: "Вы вошли как"
};
var options_log_out$2 = {
	message: "Выйти"
};
var options_log_in$2 = {
	message: "Войти"
};
var options_shortcut_title$2 = {
	message: "Сочетание клавиш"
};
var options_shortcut_record$2 = {
	message: "Задать новое сочетание клавиш"
};
var options_theme_title$2 = {
	message: "Тема"
};
var options_theme_light$2 = {
	message: "Светлый"
};
var options_theme_dark$2 = {
	message: "Темный"
};
var options_theme_system$2 = {
	message: "Использовать системные настройки"
};
var options_app_title$2 = {
	message: "Мобильное приложение Pocket"
};
var options_app_apple$2 = {
	message: "Скачать в Apple App Store"
};
var options_app_google$2 = {
	message: "Загрузить из Google Play"
};
var options_need_help$2 = {
	message: "Нужна помощь?"
};
var options_email_us$2 = {
	message: "Пишите нам"
};
var options_follow$2 = {
	message: "Следите за Pocket"
};
var options_family$2 = {
	message: "Pocket входит в семейство продуктов Mozilla."
};
var options_privacy$2 = {
	message: "Политика конфиденциальности"
};
var options_terms$2 = {
	message: "Условия использования"
};
var ru = {
	extension_description: extension_description$2,
	heading_idle: heading_idle$2,
	heading_error: heading_error$2,
	heading_saving: heading_saving$2,
	heading_saved: heading_saved$2,
	heading_save_failed: heading_save_failed$2,
	heading_removing: heading_removing$2,
	heading_removed: heading_removed$2,
	heading_remove_failed: heading_remove_failed$2,
	heading_tags_saving: heading_tags_saving$2,
	heading_tags_saved: heading_tags_saved$2,
	heading_tags_failed: heading_tags_failed$2,
	heading_tags_error: heading_tags_error$2,
	buttons_remove: buttons_remove$2,
	buttons_mylist: buttons_mylist$2,
	buttons_save: buttons_save$2,
	context_menu_open_list: context_menu_open_list$2,
	context_menu_discover_more: context_menu_discover_more$2,
	context_menu_log_in: context_menu_log_in$2,
	context_menu_log_out: context_menu_log_out$2,
	context_menu_save: context_menu_save$2,
	tagging_add_tags: tagging_add_tags$2,
	options_header: options_header$2,
	options_login_title: options_login_title$2,
	options_log_out: options_log_out$2,
	options_log_in: options_log_in$2,
	options_shortcut_title: options_shortcut_title$2,
	options_shortcut_record: options_shortcut_record$2,
	options_theme_title: options_theme_title$2,
	options_theme_light: options_theme_light$2,
	options_theme_dark: options_theme_dark$2,
	options_theme_system: options_theme_system$2,
	options_app_title: options_app_title$2,
	options_app_apple: options_app_apple$2,
	options_app_google: options_app_google$2,
	options_need_help: options_need_help$2,
	options_email_us: options_email_us$2,
	options_follow: options_follow$2,
	options_family: options_family$2,
	options_privacy: options_privacy$2,
	options_terms: options_terms$2
};

var extension_description$1 = {
	message: "捕获文章、视频等内容的最轻松、快捷方式。"
};
var heading_idle$1 = {
	message: ""
};
var heading_error$1 = {
	message: "出错了！"
};
var heading_saving$1 = {
	message: "保存..."
};
var heading_saved$1 = {
	message: "已保存到 Pocket"
};
var heading_save_failed$1 = {
	message: "出错了！"
};
var heading_removing$1 = {
	message: "正在删除..."
};
var heading_removed$1 = {
	message: "已删除"
};
var heading_remove_failed$1 = {
	message: "出错了！"
};
var heading_tags_saving$1 = {
	message: "正在保存标记……"
};
var heading_tags_saved$1 = {
	message: "标记已保存"
};
var heading_tags_failed$1 = {
	message: "出错了！"
};
var heading_tags_error$1 = {
	message: "标记限于 25 个字符"
};
var buttons_remove$1 = {
	message: "删除"
};
var buttons_mylist$1 = {
	message: "保存内容"
};
var buttons_save$1 = {
	message: "保存"
};
var context_menu_open_list$1 = {
	message: "打开您的 Pocket 保存内容"
};
var context_menu_discover_more$1 = {
	message: "在 Pocket 发现更多内容"
};
var context_menu_log_in$1 = {
	message: "登录"
};
var context_menu_log_out$1 = {
	message: "注销"
};
var context_menu_save$1 = {
	message: "保存到 Pocket"
};
var tagging_add_tags$1 = {
	message: "添加标记"
};
var options_header$1 = {
	message: "保存到 Pocket 扩展件"
};
var options_login_title$1 = {
	message: "登录为"
};
var options_log_out$1 = {
	message: "注销"
};
var options_log_in$1 = {
	message: "登录"
};
var options_shortcut_title$1 = {
	message: "键盘快捷键"
};
var options_shortcut_record$1 = {
	message: "记录新的快捷键"
};
var options_theme_title$1 = {
	message: "主题"
};
var options_theme_light$1 = {
	message: "浅色"
};
var options_theme_dark$1 = {
	message: "深色"
};
var options_theme_system$1 = {
	message: "使用系统设置"
};
var options_app_title$1 = {
	message: "Pocket 的移动应用"
};
var options_app_apple$1 = {
	message: "从 Apple App Store 下载"
};
var options_app_google$1 = {
	message: "从 Google Play 获取"
};
var options_need_help$1 = {
	message: "需要帮助？"
};
var options_email_us$1 = {
	message: "电邮我们"
};
var options_follow$1 = {
	message: "关注 Pocket"
};
var options_family$1 = {
	message: "Pocket 是 Mozilla 系列产品的一部分。"
};
var options_privacy$1 = {
	message: "隐私政策"
};
var options_terms$1 = {
	message: "服务条款"
};
var zh_CN = {
	extension_description: extension_description$1,
	heading_idle: heading_idle$1,
	heading_error: heading_error$1,
	heading_saving: heading_saving$1,
	heading_saved: heading_saved$1,
	heading_save_failed: heading_save_failed$1,
	heading_removing: heading_removing$1,
	heading_removed: heading_removed$1,
	heading_remove_failed: heading_remove_failed$1,
	heading_tags_saving: heading_tags_saving$1,
	heading_tags_saved: heading_tags_saved$1,
	heading_tags_failed: heading_tags_failed$1,
	heading_tags_error: heading_tags_error$1,
	buttons_remove: buttons_remove$1,
	buttons_mylist: buttons_mylist$1,
	buttons_save: buttons_save$1,
	context_menu_open_list: context_menu_open_list$1,
	context_menu_discover_more: context_menu_discover_more$1,
	context_menu_log_in: context_menu_log_in$1,
	context_menu_log_out: context_menu_log_out$1,
	context_menu_save: context_menu_save$1,
	tagging_add_tags: tagging_add_tags$1,
	options_header: options_header$1,
	options_login_title: options_login_title$1,
	options_log_out: options_log_out$1,
	options_log_in: options_log_in$1,
	options_shortcut_title: options_shortcut_title$1,
	options_shortcut_record: options_shortcut_record$1,
	options_theme_title: options_theme_title$1,
	options_theme_light: options_theme_light$1,
	options_theme_dark: options_theme_dark$1,
	options_theme_system: options_theme_system$1,
	options_app_title: options_app_title$1,
	options_app_apple: options_app_apple$1,
	options_app_google: options_app_google$1,
	options_need_help: options_need_help$1,
	options_email_us: options_email_us$1,
	options_follow: options_follow$1,
	options_family: options_family$1,
	options_privacy: options_privacy$1,
	options_terms: options_terms$1
};

var extension_description = {
	message: "擷取文章、短片等内容的最簡捷方法。"
};
var heading_idle = {
	message: ""
};
var heading_error = {
	message: "出了點問題！"
};
var heading_saving = {
	message: "正在儲存..."
};
var heading_saved = {
	message: "已儲存到 Pocket"
};
var heading_save_failed = {
	message: "出了點問題！"
};
var heading_removing = {
	message: "移除中..."
};
var heading_removed = {
	message: "已移除"
};
var heading_remove_failed = {
	message: "出了點問題！"
};
var heading_tags_saving = {
	message: "正在儲存標籤……"
};
var heading_tags_saved = {
	message: "標籤已儲存"
};
var heading_tags_failed = {
	message: "出了點問題！"
};
var heading_tags_error = {
	message: "標籤長度限於 25 個字元"
};
var buttons_remove = {
	message: "移除"
};
var buttons_mylist = {
	message: "儲存項目"
};
var buttons_save = {
	message: "儲存"
};
var context_menu_open_list = {
	message: "開啟您的 Pocket 儲存內容"
};
var context_menu_discover_more = {
	message: "在 Pocket 上發掘更多內容"
};
var context_menu_log_in = {
	message: "登入"
};
var context_menu_log_out = {
	message: "登出"
};
var context_menu_save = {
	message: "儲存到 Pocket"
};
var tagging_add_tags = {
	message: "新增標籤"
};
var options_header = {
	message: "儲存到 Pocket 擴充功能"
};
var options_login_title = {
	message: "已登入為"
};
var options_log_out = {
	message: "登出"
};
var options_log_in = {
	message: "登入"
};
var options_shortcut_title = {
	message: "鍵盤快速鍵"
};
var options_shortcut_record = {
	message: "記錄新捷徑"
};
var options_theme_title = {
	message: "主題"
};
var options_theme_light = {
	message: "淺色"
};
var options_theme_dark = {
	message: "暗色調"
};
var options_theme_system = {
	message: "使用系統設定"
};
var options_app_title = {
	message: "Pocket 的行動應用程式"
};
var options_app_apple = {
	message: "在 Apple App Store 下載"
};
var options_app_google = {
	message: "在 Google Play 取得"
};
var options_need_help = {
	message: "需要幫助？"
};
var options_email_us = {
	message: "電郵我們"
};
var options_follow = {
	message: "關注 Pocket"
};
var options_family = {
	message: "Pocket 屬於 Mozilla 系列產品之一。"
};
var options_privacy = {
	message: "隱私政策"
};
var options_terms = {
	message: "服務條款"
};
var zh_TW = {
	extension_description: extension_description,
	heading_idle: heading_idle,
	heading_error: heading_error,
	heading_saving: heading_saving,
	heading_saved: heading_saved,
	heading_save_failed: heading_save_failed,
	heading_removing: heading_removing,
	heading_removed: heading_removed,
	heading_remove_failed: heading_remove_failed,
	heading_tags_saving: heading_tags_saving,
	heading_tags_saved: heading_tags_saved,
	heading_tags_failed: heading_tags_failed,
	heading_tags_error: heading_tags_error,
	buttons_remove: buttons_remove,
	buttons_mylist: buttons_mylist,
	buttons_save: buttons_save,
	context_menu_open_list: context_menu_open_list,
	context_menu_discover_more: context_menu_discover_more,
	context_menu_log_in: context_menu_log_in,
	context_menu_log_out: context_menu_log_out,
	context_menu_save: context_menu_save,
	tagging_add_tags: tagging_add_tags,
	options_header: options_header,
	options_login_title: options_login_title,
	options_log_out: options_log_out,
	options_log_in: options_log_in,
	options_shortcut_title: options_shortcut_title,
	options_shortcut_record: options_shortcut_record,
	options_theme_title: options_theme_title,
	options_theme_light: options_theme_light,
	options_theme_dark: options_theme_dark,
	options_theme_system: options_theme_system,
	options_app_title: options_app_title,
	options_app_apple: options_app_apple,
	options_app_google: options_app_google,
	options_need_help: options_need_help,
	options_email_us: options_email_us,
	options_follow: options_follow,
	options_family: options_family,
	options_privacy: options_privacy,
	options_terms: options_terms
};

function getCurrentLanguageCode() {
  var language = navigator.languages ? navigator.languages[0] : navigator.language || navigator.userLanguage;
  language = typeof language !== 'undefined' ? language.toLowerCase() : 'en';
  if (language.indexOf('en') === 0) return 'en'; // English

  if (language.indexOf('de') === 0) return 'de'; // German

  if (language.indexOf('fr') === 0) return 'fr'; // French

  if (language.indexOf('it') === 0) return 'it'; // Italian

  if (language.indexOf('es_419') === 0) return 'es_419'; // Spanish (Latin America and Caribbean)

  if (language.indexOf('es') === 0) return 'es'; // Spanish

  if (language.indexOf('ja') === 0) return 'ja'; // Japanese

  if (language.indexOf('ru') === 0) return 'ru'; // Russian

  if (language.indexOf('ko') === 0) return 'ko'; // Korean

  if (language.indexOf('nl') === 0) return 'nl'; // Dutch

  if (language.indexOf('pl') === 0) return 'pl'; // Polish

  if (language.indexOf('pt_BR') === 0) return 'pt_BR'; // Portuguese Brazil

  if (language.indexOf('pt_PT') === 0) return 'pt_PT'; // Portuguese Portugal

  if (language.indexOf('zh_CN') === 0) return 'zh_CN'; // Chinese Simplified

  if (language.indexOf('zh_TW') === 0) return 'zh_TW'; // Chinese Traditional

  return 'en'; // Default is English
}

function localizedStrings() {
  const localizedCopy = {
    de,
    en,
    es,
    es_419,
    fr,
    it,
    ja,
    ko,
    nl,
    pl,
    pt_BR,
    pt_PT,
    ru,
    zh_CN,
    zh_TW
  };
  const currentLanguage = getCurrentLanguageCode();
  return localizedCopy[currentLanguage] || localizedCopy['en'];
}

const currentStrings = localizedStrings();
function localize(string) {
  var _currentStrings$strin;

  return (_currentStrings$strin = currentStrings[string]) === null || _currentStrings$strin === void 0 ? void 0 : _currentStrings$strin.message;
}

var postAuthSave = null;
/* Browser Action - Toolbar Icon Clicked
–––––––––––––––––––––––––––––––––––––––––––––––––– */

function browserAction(tab) {
  if (isSystemPage(tab)) return openPocketHome(); // open list on non-standard pages

  const {
    id: tabId,
    title,
    url: pageUrl
  } = tab;
  save({
    pageUrl,
    title,
    tabId
  });
}
/* Context Clicks - Right/Option Click Menus
–––––––––––––––––––––––––––––––––––––––––––––––––– */

function contextClick(info, tab) {
  const {
    menuItemId,
    linkUrl,
    pageUrl
  } = info;
  const {
    id: tabId,
    title
  } = tab;
  if (menuItemId === 'toolbarContextClickHome') return openPocketHome();
  if (menuItemId === 'toolbarContextClickList') return openPocketList();
  if (menuItemId === 'toolbarContextClickLogOut') return logOut();
  if (menuItemId === 'toolbarContextClickLogIn') return logIn(); // Open list on non-standard pages/links

  if (isSystemLink(linkUrl || pageUrl)) return openPocketHome();
  return save({
    linkUrl,
    pageUrl,
    title,
    tabId
  });
}
/* Saving
–––––––––––––––––––––––––––––––––––––––––––––––––– */

async function save({
  linkUrl,
  pageUrl,
  title,
  tabId
}) {
  // send message that we are requesting a save
  chrome.tabs.sendMessage(tabId, {
    action: SAVE_TO_POCKET_REQUEST
  });

  try {
    // Are we authed?
    const access_token = await getSetting('access_token');
    if (!access_token) return logIn({
      linkUrl,
      pageUrl,
      title,
      tabId
    });
    const url = linkUrl || pageUrl;
    const {
      response: payload
    } = await saveToPocket({
      url,
      title,
      tabId
    }); // send a message with the response

    const message = payload ? {
      action: SAVE_TO_POCKET_SUCCESS,
      payload
    } : {
      action: SAVE_TO_POCKET_FAILURE,
      payload
    };
    chrome.tabs.sendMessage(tabId, message);
    if (payload) saveSuccess(tabId, { ...payload,
      isLink: Boolean(linkUrl)
    });
  } catch (error) {
    // If it is an auth error let's redirect the user
    if ((error === null || error === void 0 ? void 0 : error.xErrorCode) === '107') {
      return logIn({
        linkUrl,
        pageUrl,
        title,
        tabId
      });
    } // Otherwise let's just show the error message


    const payload = {
      message: error
    };
    const errorMessage = {
      action: SAVE_TO_POCKET_FAILURE,
      payload
    };
    chrome.tabs.sendMessage(tabId, errorMessage);
  }
}
/* Remove item
–––––––––––––––––––––––––––––––––––––––––––––––––– */


async function removeItemAction(tab, payload) {
  const {
    id: tabId
  } = tab;
  const {
    itemId
  } = payload; // send message that we are attempting to sync tags

  chrome.tabs.sendMessage(tabId, {
    action: REMOVE_ITEM_REQUEST
  });
  const {
    response
  } = await removeItem(itemId);
  const message = response ? {
    action: REMOVE_ITEM_SUCCESS,
    payload
  } : {
    action: REMOVE_ITEM_FAILURE,
    payload
  };
  chrome.tabs.sendMessage(tabId, message);
  if (response) setToolbarIcon(tabId, false);
}
/* Add tags to item
–––––––––––––––––––––––––––––––––––––––––––––––––– */

async function tagsSyncAction(tab, payload) {
  const {
    id: tabId
  } = tab;
  const {
    item_id,
    tags,
    ...actionInfo
  } = payload; // send message that we are attempting to sync tags

  chrome.tabs.sendMessage(tabId, {
    action: TAG_SYNC_REQUEST
  });
  const {
    response
  } = await syncItemTags(item_id, tags, actionInfo);
  const message = response ? {
    action: TAG_SYNC_SUCCESS,
    payload
  } : {
    action: TAG_SYNC_FAILURE,
    payload
  };
  chrome.tabs.sendMessage(tabId, message);
}
/* Submit tags error
–––––––––––––––––––––––––––––––––––––––––––––––––– */

async function tagsErrorAction(tab, payload) {
  const {
    id: tabId
  } = tab;
  chrome.tabs.sendMessage(tabId, {
    action: UPDATE_TAG_ERROR,
    payload
  });
}
/* Authentication user
–––––––––––––––––––––––––––––––––––––––––––––––––– */

async function authCodeRecieved(tab, payload) {
  // Getting a Guid to use in the request
  // Getting an auth token
  try {
    const guidResponse = await getGuid();
    const authResponse = await authorize(guidResponse, payload);
    const {
      access_token,
      account,
      username
    } = authResponse;
    const {
      premium_status
    } = account;
    setSettings({
      access_token,
      premium_status,
      username
    });
  } catch (err) {
    withScope(scope => {
      scope.setFingerprint('Auth Error');
      captureMessage(err);
    });
  }

  closeLoginPage();
  setContextMenus();
  if (postAuthSave) save(postAuthSave);
  postAuthSave = null;
}
function logOut() {
  chrome.tabs.create({
    url: LOGOUT_URL
  });
}
function loggedOutOfPocket() {
  chrome.storage.local.clear();
  setContextMenus();
}
function logIn(saveObject) {
  postAuthSave = saveObject;
  chrome.tabs.create({
    url: AUTH_URL
  });
}
function openPocket() {
  chrome.tabs.create({
    url: POCKET_LIST
  });
}
function openPocketList() {
  chrome.tabs.create({
    url: POCKET_LIST
  });
}
function openPocketHome() {
  chrome.tabs.create({
    url: POCKET_HOME
  });
}
function openOptionsPage() {
  chrome.runtime.openOptionsPage();
}
/* Tab Changes
–––––––––––––––––––––––––––––––––––––––––––––––––– */

function tabUpdated(tabId, changeInfo) {
  if (changeInfo.status === 'loading' && changeInfo.url) {
    // if actively loading a new page, unset save state on icon
    setToolbarIcon(tabId, false);
  }
}
/* Theme Changes
–––––––––––––––––––––––––––––––––––––––––––––––––– */

async function setColorMode(tab, {
  theme
}) {
  await setSettings({
    theme
  });
}
/* Context Menus
–––––––––––––––––––––––––––––––––––––––––––––––––– */

async function setContextMenus() {
  chrome.contextMenus.removeAll(); // Page Context - Right click menu on page

  chrome.contextMenus.create({
    title: localize('context_menu_save'),
    id: 'pageContextClick',
    contexts: ['page', 'frame', 'editable', 'image', 'video', 'audio', 'link', 'selection'] // prettier-ignore

  }); // Browser Icon - Right click menu

  chrome.contextMenus.create({
    title: localize('context_menu_open_list'),
    id: 'toolbarContextClickList',
    contexts: ['action']
  });
  chrome.contextMenus.create({
    title: localize('context_menu_discover_more'),
    id: 'toolbarContextClickHome',
    contexts: ['action']
  }); // Log In or Out menu item depending on existence of access token

  const access_token = await getSetting('access_token');

  if (access_token) {
    chrome.contextMenus.create({
      title: localize('context_menu_log_out'),
      id: 'toolbarContextClickLogOut',
      contexts: ['action']
    });
  } else {
    chrome.contextMenus.create({
      title: localize('context_menu_log_in'),
      id: 'toolbarContextClickLogIn',
      contexts: ['action']
    });
  }
}

/*! *****************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */
/* global Reflect, Promise */

var extendStatics = function(d, b) {
    extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return extendStatics(d, b);
};

function __extends(d, b) {
    extendStatics(d, b);
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
}

var __assign = function() {
    __assign = Object.assign || function __assign(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p)) t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};

function __read(o, n) {
    var m = typeof Symbol === "function" && o[Symbol.iterator];
    if (!m) return o;
    var i = m.call(o), r, ar = [], e;
    try {
        while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
    }
    catch (error) { e = { error: error }; }
    finally {
        try {
            if (r && !r.done && (m = i["return"])) m.call(i);
        }
        finally { if (e) throw e.error; }
    }
    return ar;
}

function __spread() {
    for (var ar = [], i = 0; i < arguments.length; i++)
        ar = ar.concat(__read(arguments[i]));
    return ar;
}

/** The status of an Span. */
// eslint-disable-next-line import/export
var SpanStatus;
(function (SpanStatus) {
    /** The operation completed successfully. */
    SpanStatus["Ok"] = "ok";
    /** Deadline expired before operation could complete. */
    SpanStatus["DeadlineExceeded"] = "deadline_exceeded";
    /** 401 Unauthorized (actually does mean unauthenticated according to RFC 7235) */
    SpanStatus["Unauthenticated"] = "unauthenticated";
    /** 403 Forbidden */
    SpanStatus["PermissionDenied"] = "permission_denied";
    /** 404 Not Found. Some requested entity (file or directory) was not found. */
    SpanStatus["NotFound"] = "not_found";
    /** 429 Too Many Requests */
    SpanStatus["ResourceExhausted"] = "resource_exhausted";
    /** Client specified an invalid argument. 4xx. */
    SpanStatus["InvalidArgument"] = "invalid_argument";
    /** 501 Not Implemented */
    SpanStatus["Unimplemented"] = "unimplemented";
    /** 503 Service Unavailable */
    SpanStatus["Unavailable"] = "unavailable";
    /** Other/generic 5xx. */
    SpanStatus["InternalError"] = "internal_error";
    /** Unknown. Any non-standard HTTP status code. */
    SpanStatus["UnknownError"] = "unknown_error";
    /** The operation was cancelled (typically by the user). */
    SpanStatus["Cancelled"] = "cancelled";
    /** Already exists (409) */
    SpanStatus["AlreadyExists"] = "already_exists";
    /** Operation was rejected because the system is not in a state required for the operation's */
    SpanStatus["FailedPrecondition"] = "failed_precondition";
    /** The operation was aborted, typically due to a concurrency issue. */
    SpanStatus["Aborted"] = "aborted";
    /** Operation was attempted past the valid range. */
    SpanStatus["OutOfRange"] = "out_of_range";
    /** Unrecoverable data loss or corruption */
    SpanStatus["DataLoss"] = "data_loss";
})(SpanStatus || (SpanStatus = {}));
// eslint-disable-next-line @typescript-eslint/no-namespace, import/export
(function (SpanStatus) {
    /**
     * Converts a HTTP status code into a {@link SpanStatus}.
     *
     * @param httpStatus The HTTP response status code.
     * @returns The span status or {@link SpanStatus.UnknownError}.
     */
    function fromHttpCode(httpStatus) {
        if (httpStatus < 400 && httpStatus >= 100) {
            return SpanStatus.Ok;
        }
        if (httpStatus >= 400 && httpStatus < 500) {
            switch (httpStatus) {
                case 401:
                    return SpanStatus.Unauthenticated;
                case 403:
                    return SpanStatus.PermissionDenied;
                case 404:
                    return SpanStatus.NotFound;
                case 409:
                    return SpanStatus.AlreadyExists;
                case 413:
                    return SpanStatus.FailedPrecondition;
                case 429:
                    return SpanStatus.ResourceExhausted;
                default:
                    return SpanStatus.InvalidArgument;
            }
        }
        if (httpStatus >= 500 && httpStatus < 600) {
            switch (httpStatus) {
                case 501:
                    return SpanStatus.Unimplemented;
                case 503:
                    return SpanStatus.Unavailable;
                case 504:
                    return SpanStatus.DeadlineExceeded;
                default:
                    return SpanStatus.InternalError;
            }
        }
        return SpanStatus.UnknownError;
    }
    SpanStatus.fromHttpCode = fromHttpCode;
})(SpanStatus || (SpanStatus = {}));

/**
 * Determines if tracing is currently enabled.
 *
 * Tracing is enabled when at least one of `tracesSampleRate` and `tracesSampler` is defined in the SDK config.
 */
function hasTracingEnabled(options) {
    if (options === void 0) { options = (_a = getCurrentHub()
        .getClient()) === null || _a === void 0 ? void 0 : _a.getOptions(); }
    var _a;
    return !!options && ('tracesSampleRate' in options || 'tracesSampler' in options);
}
/** Grabs active transaction off scope, if any */
function getActiveTransaction(hub) {
    if (hub === void 0) { hub = getCurrentHub(); }
    var _a, _b;
    return (_b = (_a = hub) === null || _a === void 0 ? void 0 : _a.getScope()) === null || _b === void 0 ? void 0 : _b.getTransaction();
}

/**
 * Configures global error listeners
 */
function registerErrorInstrumentation() {
    addInstrumentationHandler({
        callback: errorCallback,
        type: 'error',
    });
    addInstrumentationHandler({
        callback: errorCallback,
        type: 'unhandledrejection',
    });
}
/**
 * If an error or unhandled promise occurs, we mark the active transaction as failed
 */
function errorCallback() {
    var activeTransaction = getActiveTransaction();
    if (activeTransaction) {
        logger.log("[Tracing] Transaction: " + SpanStatus.InternalError + " -> Global error occured");
        activeTransaction.setStatus(SpanStatus.InternalError);
    }
}

/**
 * Keeps track of finished spans for a given transaction
 * @internal
 * @hideconstructor
 * @hidden
 */
var SpanRecorder = /** @class */ (function () {
    function SpanRecorder(maxlen) {
        if (maxlen === void 0) { maxlen = 1000; }
        this.spans = [];
        this._maxlen = maxlen;
    }
    /**
     * This is just so that we don't run out of memory while recording a lot
     * of spans. At some point we just stop and flush out the start of the
     * trace tree (i.e.the first n spans with the smallest
     * start_timestamp).
     */
    SpanRecorder.prototype.add = function (span) {
        if (this.spans.length > this._maxlen) {
            span.spanRecorder = undefined;
        }
        else {
            this.spans.push(span);
        }
    };
    return SpanRecorder;
}());
/**
 * Span contains all data about a span
 */
var Span = /** @class */ (function () {
    /**
     * You should never call the constructor manually, always use `Sentry.startTransaction()`
     * or call `startChild()` on an existing span.
     * @internal
     * @hideconstructor
     * @hidden
     */
    function Span(spanContext) {
        /**
         * @inheritDoc
         */
        this.traceId = uuid4();
        /**
         * @inheritDoc
         */
        this.spanId = uuid4().substring(16);
        /**
         * Timestamp in seconds when the span was created.
         */
        this.startTimestamp = timestampWithMs();
        /**
         * @inheritDoc
         */
        this.tags = {};
        /**
         * @inheritDoc
         */
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        this.data = {};
        if (!spanContext) {
            return this;
        }
        if (spanContext.traceId) {
            this.traceId = spanContext.traceId;
        }
        if (spanContext.spanId) {
            this.spanId = spanContext.spanId;
        }
        if (spanContext.parentSpanId) {
            this.parentSpanId = spanContext.parentSpanId;
        }
        // We want to include booleans as well here
        if ('sampled' in spanContext) {
            this.sampled = spanContext.sampled;
        }
        if (spanContext.op) {
            this.op = spanContext.op;
        }
        if (spanContext.description) {
            this.description = spanContext.description;
        }
        if (spanContext.data) {
            this.data = spanContext.data;
        }
        if (spanContext.tags) {
            this.tags = spanContext.tags;
        }
        if (spanContext.status) {
            this.status = spanContext.status;
        }
        if (spanContext.startTimestamp) {
            this.startTimestamp = spanContext.startTimestamp;
        }
        if (spanContext.endTimestamp) {
            this.endTimestamp = spanContext.endTimestamp;
        }
    }
    /**
     * @inheritDoc
     * @deprecated
     */
    Span.prototype.child = function (spanContext) {
        return this.startChild(spanContext);
    };
    /**
     * @inheritDoc
     */
    Span.prototype.startChild = function (spanContext) {
        var childSpan = new Span(__assign(__assign({}, spanContext), { parentSpanId: this.spanId, sampled: this.sampled, traceId: this.traceId }));
        childSpan.spanRecorder = this.spanRecorder;
        if (childSpan.spanRecorder) {
            childSpan.spanRecorder.add(childSpan);
        }
        childSpan.transaction = this.transaction;
        return childSpan;
    };
    /**
     * @inheritDoc
     */
    Span.prototype.setTag = function (key, value) {
        var _a;
        this.tags = __assign(__assign({}, this.tags), (_a = {}, _a[key] = value, _a));
        return this;
    };
    /**
     * @inheritDoc
     */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/explicit-module-boundary-types
    Span.prototype.setData = function (key, value) {
        var _a;
        this.data = __assign(__assign({}, this.data), (_a = {}, _a[key] = value, _a));
        return this;
    };
    /**
     * @inheritDoc
     */
    Span.prototype.setStatus = function (value) {
        this.status = value;
        return this;
    };
    /**
     * @inheritDoc
     */
    Span.prototype.setHttpStatus = function (httpStatus) {
        this.setTag('http.status_code', String(httpStatus));
        var spanStatus = SpanStatus.fromHttpCode(httpStatus);
        if (spanStatus !== SpanStatus.UnknownError) {
            this.setStatus(spanStatus);
        }
        return this;
    };
    /**
     * @inheritDoc
     */
    Span.prototype.isSuccess = function () {
        return this.status === SpanStatus.Ok;
    };
    /**
     * @inheritDoc
     */
    Span.prototype.finish = function (endTimestamp) {
        this.endTimestamp = typeof endTimestamp === 'number' ? endTimestamp : timestampWithMs();
    };
    /**
     * @inheritDoc
     */
    Span.prototype.toTraceparent = function () {
        var sampledString = '';
        if (this.sampled !== undefined) {
            sampledString = this.sampled ? '-1' : '-0';
        }
        return this.traceId + "-" + this.spanId + sampledString;
    };
    /**
     * @inheritDoc
     */
    Span.prototype.toContext = function () {
        return dropUndefinedKeys({
            data: this.data,
            description: this.description,
            endTimestamp: this.endTimestamp,
            op: this.op,
            parentSpanId: this.parentSpanId,
            sampled: this.sampled,
            spanId: this.spanId,
            startTimestamp: this.startTimestamp,
            status: this.status,
            tags: this.tags,
            traceId: this.traceId,
        });
    };
    /**
     * @inheritDoc
     */
    Span.prototype.updateWithContext = function (spanContext) {
        var _a, _b, _c, _d, _e;
        this.data = (_a = spanContext.data, (_a !== null && _a !== void 0 ? _a : {}));
        this.description = spanContext.description;
        this.endTimestamp = spanContext.endTimestamp;
        this.op = spanContext.op;
        this.parentSpanId = spanContext.parentSpanId;
        this.sampled = spanContext.sampled;
        this.spanId = (_b = spanContext.spanId, (_b !== null && _b !== void 0 ? _b : this.spanId));
        this.startTimestamp = (_c = spanContext.startTimestamp, (_c !== null && _c !== void 0 ? _c : this.startTimestamp));
        this.status = spanContext.status;
        this.tags = (_d = spanContext.tags, (_d !== null && _d !== void 0 ? _d : {}));
        this.traceId = (_e = spanContext.traceId, (_e !== null && _e !== void 0 ? _e : this.traceId));
        return this;
    };
    /**
     * @inheritDoc
     */
    Span.prototype.getTraceContext = function () {
        return dropUndefinedKeys({
            data: Object.keys(this.data).length > 0 ? this.data : undefined,
            description: this.description,
            op: this.op,
            parent_span_id: this.parentSpanId,
            span_id: this.spanId,
            status: this.status,
            tags: Object.keys(this.tags).length > 0 ? this.tags : undefined,
            trace_id: this.traceId,
        });
    };
    /**
     * @inheritDoc
     */
    Span.prototype.toJSON = function () {
        return dropUndefinedKeys({
            data: Object.keys(this.data).length > 0 ? this.data : undefined,
            description: this.description,
            op: this.op,
            parent_span_id: this.parentSpanId,
            span_id: this.spanId,
            start_timestamp: this.startTimestamp,
            status: this.status,
            tags: Object.keys(this.tags).length > 0 ? this.tags : undefined,
            timestamp: this.endTimestamp,
            trace_id: this.traceId,
        });
    };
    return Span;
}());

/** JSDoc */
var Transaction = /** @class */ (function (_super) {
    __extends(Transaction, _super);
    /**
     * This constructor should never be called manually. Those instrumenting tracing should use
     * `Sentry.startTransaction()`, and internal methods should use `hub.startTransaction()`.
     * @internal
     * @hideconstructor
     * @hidden
     */
    function Transaction(transactionContext, hub) {
        var _this = _super.call(this, transactionContext) || this;
        _this._measurements = {};
        /**
         * The reference to the current hub.
         */
        _this._hub = getCurrentHub();
        if (isInstanceOf(hub, Hub)) {
            _this._hub = hub;
        }
        _this.name = transactionContext.name || '';
        _this.metadata = transactionContext.metadata || {};
        _this._trimEnd = transactionContext.trimEnd;
        // this is because transactions are also spans, and spans have a transaction pointer
        _this.transaction = _this;
        return _this;
    }
    /**
     * JSDoc
     */
    Transaction.prototype.setName = function (name) {
        this.name = name;
    };
    /**
     * Attaches SpanRecorder to the span itself
     * @param maxlen maximum number of spans that can be recorded
     */
    Transaction.prototype.initSpanRecorder = function (maxlen) {
        if (maxlen === void 0) { maxlen = 1000; }
        if (!this.spanRecorder) {
            this.spanRecorder = new SpanRecorder(maxlen);
        }
        this.spanRecorder.add(this);
    };
    /**
     * Set observed measurements for this transaction.
     * @hidden
     */
    Transaction.prototype.setMeasurements = function (measurements) {
        this._measurements = __assign({}, measurements);
    };
    /**
     * Set metadata for this transaction.
     * @hidden
     */
    Transaction.prototype.setMetadata = function (newMetadata) {
        this.metadata = __assign(__assign({}, this.metadata), newMetadata);
    };
    /**
     * @inheritDoc
     */
    Transaction.prototype.finish = function (endTimestamp) {
        var _this = this;
        var _a, _b, _c, _d, _e;
        // This transaction is already finished, so we should not flush it again.
        if (this.endTimestamp !== undefined) {
            return undefined;
        }
        if (!this.name) {
            logger.warn('Transaction has no name, falling back to `<unlabeled transaction>`.');
            this.name = '<unlabeled transaction>';
        }
        // just sets the end timestamp
        _super.prototype.finish.call(this, endTimestamp);
        if (this.sampled !== true) {
            // At this point if `sampled !== true` we want to discard the transaction.
            logger.log('[Tracing] Discarding transaction because its trace was not chosen to be sampled.');
            (_e = (_c = (_a = this._hub
                .getClient()) === null || _a === void 0 ? void 0 : (_b = _a).getTransport) === null || _c === void 0 ? void 0 : (_d = _c.call(_b)).recordLostEvent) === null || _e === void 0 ? void 0 : _e.call(_d, Outcome.SampleRate, 'transaction');
            return undefined;
        }
        var finishedSpans = this.spanRecorder ? this.spanRecorder.spans.filter(function (s) { return s !== _this && s.endTimestamp; }) : [];
        if (this._trimEnd && finishedSpans.length > 0) {
            this.endTimestamp = finishedSpans.reduce(function (prev, current) {
                if (prev.endTimestamp && current.endTimestamp) {
                    return prev.endTimestamp > current.endTimestamp ? prev : current;
                }
                return prev;
            }).endTimestamp;
        }
        var transaction = {
            contexts: {
                trace: this.getTraceContext(),
            },
            spans: finishedSpans,
            start_timestamp: this.startTimestamp,
            tags: this.tags,
            timestamp: this.endTimestamp,
            transaction: this.name,
            type: 'transaction',
            debug_meta: this.metadata,
        };
        var hasMeasurements = Object.keys(this._measurements).length > 0;
        if (hasMeasurements) {
            logger.log('[Measurements] Adding measurements to transaction', JSON.stringify(this._measurements, undefined, 2));
            transaction.measurements = this._measurements;
        }
        logger.log("[Tracing] Finishing " + this.op + " transaction: " + this.name + ".");
        return this._hub.captureEvent(transaction);
    };
    /**
     * @inheritDoc
     */
    Transaction.prototype.toContext = function () {
        var spanContext = _super.prototype.toContext.call(this);
        return dropUndefinedKeys(__assign(__assign({}, spanContext), { name: this.name, trimEnd: this._trimEnd }));
    };
    /**
     * @inheritDoc
     */
    Transaction.prototype.updateWithContext = function (transactionContext) {
        var _a;
        _super.prototype.updateWithContext.call(this, transactionContext);
        this.name = (_a = transactionContext.name, (_a !== null && _a !== void 0 ? _a : ''));
        this._trimEnd = transactionContext.trimEnd;
        return this;
    };
    return Transaction;
}(Span));

/** Returns all trace headers that are currently on the top scope. */
function traceHeaders() {
    var scope = this.getScope();
    if (scope) {
        var span = scope.getSpan();
        if (span) {
            return {
                'sentry-trace': span.toTraceparent(),
            };
        }
    }
    return {};
}
/**
 * Makes a sampling decision for the given transaction and stores it on the transaction.
 *
 * Called every time a transaction is created. Only transactions which emerge with a `sampled` value of `true` will be
 * sent to Sentry.
 *
 * @param hub: The hub off of which to read config options
 * @param transaction: The transaction needing a sampling decision
 * @param samplingContext: Default and user-provided data which may be used to help make the decision
 *
 * @returns The given transaction with its `sampled` value set
 */
function sample(transaction, options, samplingContext) {
    // nothing to do if tracing is not enabled
    if (!hasTracingEnabled(options)) {
        transaction.sampled = false;
        return transaction;
    }
    // if the user has forced a sampling decision by passing a `sampled` value in their transaction context, go with that
    if (transaction.sampled !== undefined) {
        transaction.setMetadata({
            transactionSampling: { method: TransactionSamplingMethod.Explicit },
        });
        return transaction;
    }
    // we would have bailed already if neither `tracesSampler` nor `tracesSampleRate` were defined, so one of these should
    // work; prefer the hook if so
    var sampleRate;
    if (typeof options.tracesSampler === 'function') {
        sampleRate = options.tracesSampler(samplingContext);
        transaction.setMetadata({
            transactionSampling: {
                method: TransactionSamplingMethod.Sampler,
                // cast to number in case it's a boolean
                rate: Number(sampleRate),
            },
        });
    }
    else if (samplingContext.parentSampled !== undefined) {
        sampleRate = samplingContext.parentSampled;
        transaction.setMetadata({
            transactionSampling: { method: TransactionSamplingMethod.Inheritance },
        });
    }
    else {
        sampleRate = options.tracesSampleRate;
        transaction.setMetadata({
            transactionSampling: {
                method: TransactionSamplingMethod.Rate,
                // cast to number in case it's a boolean
                rate: Number(sampleRate),
            },
        });
    }
    // Since this is coming from the user (or from a function provided by the user), who knows what we might get. (The
    // only valid values are booleans or numbers between 0 and 1.)
    if (!isValidSampleRate(sampleRate)) {
        logger.warn("[Tracing] Discarding transaction because of invalid sample rate.");
        transaction.sampled = false;
        return transaction;
    }
    // if the function returned 0 (or false), or if `tracesSampleRate` is 0, it's a sign the transaction should be dropped
    if (!sampleRate) {
        logger.log("[Tracing] Discarding transaction because " + (typeof options.tracesSampler === 'function'
            ? 'tracesSampler returned 0 or false'
            : 'a negative sampling decision was inherited or tracesSampleRate is set to 0'));
        transaction.sampled = false;
        return transaction;
    }
    // Now we roll the dice. Math.random is inclusive of 0, but not of 1, so strict < is safe here. In case sampleRate is
    // a boolean, the < comparison will cause it to be automatically cast to 1 if it's true and 0 if it's false.
    transaction.sampled = Math.random() < sampleRate;
    // if we're not going to keep it, we're done
    if (!transaction.sampled) {
        logger.log("[Tracing] Discarding transaction because it's not included in the random sample (sampling rate = " + Number(sampleRate) + ")");
        return transaction;
    }
    logger.log("[Tracing] starting " + transaction.op + " transaction - " + transaction.name);
    return transaction;
}
/**
 * Checks the given sample rate to make sure it is valid type and value (a boolean, or a number between 0 and 1).
 */
function isValidSampleRate(rate) {
    // we need to check NaN explicitly because it's of type 'number' and therefore wouldn't get caught by this typecheck
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    if (isNaN(rate) || !(typeof rate === 'number' || typeof rate === 'boolean')) {
        logger.warn("[Tracing] Given sample rate is invalid. Sample rate must be a boolean or a number between 0 and 1. Got " + JSON.stringify(rate) + " of type " + JSON.stringify(typeof rate) + ".");
        return false;
    }
    // in case sampleRate is a boolean, it will get automatically cast to 1 if it's true and 0 if it's false
    if (rate < 0 || rate > 1) {
        logger.warn("[Tracing] Given sample rate is invalid. Sample rate must be between 0 and 1. Got " + rate + ".");
        return false;
    }
    return true;
}
/**
 * Creates a new transaction and adds a sampling decision if it doesn't yet have one.
 *
 * The Hub.startTransaction method delegates to this method to do its work, passing the Hub instance in as `this`, as if
 * it had been called on the hub directly. Exists as a separate function so that it can be injected into the class as an
 * "extension method."
 *
 * @param this: The Hub starting the transaction
 * @param transactionContext: Data used to configure the transaction
 * @param CustomSamplingContext: Optional data to be provided to the `tracesSampler` function (if any)
 *
 * @returns The new transaction
 *
 * @see {@link Hub.startTransaction}
 */
function _startTransaction(transactionContext, customSamplingContext) {
    var _a, _b;
    var options = ((_a = this.getClient()) === null || _a === void 0 ? void 0 : _a.getOptions()) || {};
    var transaction = new Transaction(transactionContext, this);
    transaction = sample(transaction, options, __assign({ parentSampled: transactionContext.parentSampled, transactionContext: transactionContext }, customSamplingContext));
    if (transaction.sampled) {
        transaction.initSpanRecorder((_b = options._experiments) === null || _b === void 0 ? void 0 : _b.maxSpans);
    }
    return transaction;
}
/**
 * @private
 */
function _addTracingExtensions() {
    var carrier = getMainCarrier();
    if (!carrier.__SENTRY__) {
        return;
    }
    carrier.__SENTRY__.extensions = carrier.__SENTRY__.extensions || {};
    if (!carrier.__SENTRY__.extensions.startTransaction) {
        carrier.__SENTRY__.extensions.startTransaction = _startTransaction;
    }
    if (!carrier.__SENTRY__.extensions.traceHeaders) {
        carrier.__SENTRY__.extensions.traceHeaders = traceHeaders;
    }
}
/**
 * @private
 */
function _autoloadDatabaseIntegrations() {
    var carrier = getMainCarrier();
    if (!carrier.__SENTRY__) {
        return;
    }
    var packageToIntegrationMapping = {
        mongodb: function () {
            var integration = dynamicRequire(module, './integrations/node/mongo');
            return new integration.Mongo();
        },
        mongoose: function () {
            var integration = dynamicRequire(module, './integrations/node/mongo');
            return new integration.Mongo({ mongoose: true });
        },
        mysql: function () {
            var integration = dynamicRequire(module, './integrations/node/mysql');
            return new integration.Mysql();
        },
        pg: function () {
            var integration = dynamicRequire(module, './integrations/node/postgres');
            return new integration.Postgres();
        },
    };
    var mappedPackages = Object.keys(packageToIntegrationMapping)
        .filter(function (moduleName) { return !!loadModule(moduleName); })
        .map(function (pkg) {
        try {
            return packageToIntegrationMapping[pkg]();
        }
        catch (e) {
            return undefined;
        }
    })
        .filter(function (p) { return p; });
    if (mappedPackages.length > 0) {
        carrier.__SENTRY__.integrations = __spread((carrier.__SENTRY__.integrations || []), mappedPackages);
    }
}
/**
 * This patches the global object and injects the Tracing extensions methods
 */
function addExtensionMethods() {
    _addTracingExtensions();
    // Detect and automatically load specified integrations.
    if (isNodeEnv()) {
        _autoloadDatabaseIntegrations();
    }
    // If an error happens globally, we should make sure transaction status is set to error.
    registerErrorInstrumentation();
}

// We are patching the global object with our hub extension methods
addExtensionMethods();

init({
  dsn: 'https://11eed553982148d5b0b0288798aa3d85@o28549.ingest.sentry.io/6120053',
  tracesSampleRate: 0,
  sampleRate: 0.5
});
/* Initial Setup
–––––––––––––––––––––––––––––––––––––––––––––––––– */

chrome.runtime.onInstalled.addListener(function () {
  // Use SVG icons over the png for more control
  setDefaultIcon();
  setContextMenus();
});
/* Browser Action - Toolbar
–––––––––––––––––––––––––––––––––––––––––––––––––– */

chrome.action.onClicked.addListener(browserAction);
chrome.commands.onCommand.addListener((command, tab) => {
  if (command === 'save-to-pocket-action') browserAction(tab);
});
/* Context Menus Handling
–––––––––––––––––––––––––––––––––––––––––––––––––– */

chrome.contextMenus.onClicked.addListener(contextClick);
/* Tab Handling
–––––––––––––––––––––––––––––––––––––––––––––––––– */
// Update the icon to unsaved if we are change pages

chrome.tabs.onUpdated.addListener(tabUpdated);
chrome.runtime.onMessage.addListener(function (message, sender) {
  const {
    type,
    payload
  } = message;
  const {
    tab
  } = sender;
  console.groupCollapsed(`RECEIVE: ${type}`);
  console.log(payload);
  console.groupEnd(`RECEIVE: ${type}`);

  switch (type) {
    case AUTH_CODE_RECEIVED:
      authCodeRecieved(tab, payload);
      return;

    case USER_LOG_IN:
      logIn(tab);
      return;

    case LOGGED_OUT_OF_POCKET:
      loggedOutOfPocket();
      return;

    case REMOVE_ITEM:
      removeItemAction(tab, payload);
      return;

    case RESAVE_ITEM:
      browserAction(tab);
      return;

    case TAGS_SYNC:
      tagsSyncAction(tab, payload);
      return;

    case SEND_TAG_ERROR:
      tagsErrorAction(tab, payload);
      return;

    case COLOR_MODE_CHANGE:
      setColorMode(tab, payload);
      return;

    case OPEN_POCKET:
      openPocket();
      return;

    case OPEN_OPTIONS:
      openOptionsPage();
      return;

    default:
      return Promise.resolve(`Message received: ${type}`);
  }
});
