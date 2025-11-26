import {
    storage,
    runtime,
    tabs
} from "webextension-polyfill"

import $ from "jquery"
import global from "./global";
import { AppInsightInstance, AppInsightEvent } from "./AppInsight";
var activeUBMTimer = undefined
export class Utils { 
    static str2ab(str) {
        var buf = str.split(",")
        var bufView = new Uint8Array(buf.length);
        for (var i = 0, strLen = str.length; i < strLen; i++) {
            bufView[i] = buf[i];
        }
        return bufView;
    }
    
    static isValidTopLevelNavigation(details) {
        const { url } = details;
    
        return details.frameId === 0 &&
            details.tabId > 0 &&
            url.startsWith('http') &&
            // TODO note this in the "not scanned" text for Chrome
            !url.startsWith('https://chrome.google.com/webstore/');
    }

    static getActiveTab() { 
        return tabs.query({active:true, currentWindow: true})
    }
}

export async function getValueFromStorage(key) {
    const value = await storage.local.get()
    if (value[key]) {
        return value[key]
    }
    return
}

export function setValueToStorage(key, value) {
    let jsonObj = {}
    jsonObj[key] = value

    try {
        storage.local.set(jsonObj)
        return Promise.resolve(true)
    } catch (error) {
        return Promise.reject()
    }
}

export function removeItemOnce(arr, value) {
    var index = arr.indexOf(value);
    if (index > -1) {
        arr.splice(index, 1);
    }
    return arr;
}

export function sendActive() { 
    getValueFromStorage("kActiveUBM").then(time => {
        let currentTime = Date.now()
        if (!time || currentTime - time > global.ONE_DAY ) {
            activeUBMTimer = currentTime
            AppInsightInstance.trackEvent(AppInsightEvent.extensionActive)
            setValueToStorage("kActiveUBM", activeUBMTimer) 
        } 
    })
}

export function sendFeedback(feedback) {
    let osVersion = global.BROWSER_INFO.os
    let version = runtime.getManifest().version
    let browserVersion = global.BROWSER_INFO.name + "" + global.BROWSER_INFO.version
    let body = {
        "app_name": "Trend Micro Ad Blocker For Chrome",
        "app_version": version,
        "app_build_number": "0",
        "app_bundle_id": "0",
        "mac_os_version": osVersion + " " + browserVersion,
        "feedback_comments": feedback.comments,
        "user_email": feedback.email,
        "category": feedback.category
    }
    const baseURL = "https://api.ta.trendmicro.com/1/userFeedback/form/"
    $.ajax({
        type: "POST",
        url: baseURL,
        data: body,
        dataType: "json",
        success: () => { 

        }
    })

}

export async function getCurrentTab() {
    let queryOptions = { active: true };
    // `tab` will either be a `tabs.Tab` instance or `undefined`.
    let [tab] = await tabs.query(queryOptions);
    if (tab) { 
        return tab
    }
    assert(false)
  }