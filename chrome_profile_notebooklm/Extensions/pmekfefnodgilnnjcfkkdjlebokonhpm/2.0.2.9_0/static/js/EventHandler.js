/**
 * EventHandler.js
 *
 * Trend Micro Ad Blocker For Chrome 
 *
 * Created on 2022/01/26
 * Copyright 2022 Trend Micro, Inc. All rights reserved.
 *
 */
import AOLog from './AOLog';
import { parse } from "tldts-experimental";

import global from "./global";
import { Request } from "@cliqz/adblocker";
import { Utils,sendActive } from "./Utils";
import { tabs, runtime, storage } from "webextension-polyfill";
import action from "./AOBrowserAction"
class EventHandler { 
    constructor() { 
       
    }

    onRuleMatchedDebug(info) {
        AOLog.debug("RequestUrl: " + info.request.url);
        AOLog.debug("RuleInfo: " + info.rule.rulesetId + "\t" + info.rule.ruleId)
    }

    onBeforeNavigate(details) { 
        const { tabId, frameId, url } = details
        //frameId === 0 indicates this is a main_frame
        if (frameId === 0) { 
            AOLog.verbose(`Tab ${tabId} navigate to ${url}`)
            action.update(tabId)
        }
    }

    onCommitted(details) { 
        const { tabId, frameId, transitionType, transitionQualifiers } = details;
        if (frameId === 0) { 
            action.update(tabId)
        }
    }

    onTabReplaced(addedTabId, removedTabId) { 
        action.update(addedTabId)
    }

    onTabActivated(activeInfo) {
        action.update(activeInfo.tabId) 
    }

    static fromWebRequestDetails(details) { 
        const url = details.url
        const hostname = parse(url).hostname
        const domain = parse(url).domain

        const sourceUrl = details.initiator || details.originUrl || details.documentUrl;
        const sourceDomain = parse(sourceUrl).domain
        const sourceHostname = parse(sourceUrl).hostname

        return Request.fromRawDetails(sourceDomain ? {
            url: url,
            type: details.type,
            tabId: details.tabId,
            requestId: details.requestId,
            hostname: hostname,
            domain: domain,
            sourceUrl: sourceUrl,
            sourceDomain: sourceDomain,
            sourceHostname: sourceHostname,
            _originalRequestDetails: details
        } : {
            url: url,
            type: details.type,
            tabId: details.tabId,
            requestId: details.requestId,
            hostname: hostname,
            domain: domain,
            _originalRequestDetails: details 
        })  
    }

}



export default new EventHandler()