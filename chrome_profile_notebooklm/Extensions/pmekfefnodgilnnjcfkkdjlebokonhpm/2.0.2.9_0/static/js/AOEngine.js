/**
 * AOEngine.js
 *
 * Trend Micro Ad Blocker For Chrome 
 *
 * Created on 2022/02/09
 * Copyright 2022 Trend Micro, Inc. All rights reserved.
 *
 */
import { FiltersEngine, Request } from '@cliqz/adblocker';
import { fetchLists, fetchWithRetry } from '@cliqz/adblocker';
import { parse } from 'tldts-experimental';
import { browser, storage, declarativeNetRequest} from 'webextension-polyfill';
import unblockListManager from "./AOUnblockedList";
import global from './global';

export class AOEngine extends FiltersEngine { 
    // enabled
    // blockingCallback
    // engineName

    static fromLists(fetch, urls, config = {}, caching) {
        return this.fromCached(() => {
            const listsPromises = fetchLists(fetch, urls);
            const resourcesPromise = this.fetchResources(fetch);
            return Promise.all([listsPromises,resourcesPromise]).then(([lists,resources]) => {
                const engine = this.parse(lists.join('\n'), config);
                if (resources !== undefined) {
                    engine.updateResources(resources, '' + resources.length);
                }
                return engine;
            }).catch(err => { 
                console.log(err)
            });
        }, caching);
    }

    static fetchResources(fetch) {
        var resourceURL = "https://raw.githubusercontent.com/cliqz-oss/adblocker/master/packages/adblocker/assets/ublock-origin/resources.txt"
        if (navigator.languages.includes("zh-CN") || navigator.languages.includes("zh")) { 
            resourceURL = "https://res.appletuner.trendmicro.com/AdBlockOne/resources.txt"
        }
        return this.fetchResource(fetch, resourceURL);
    }

    static fetchResource(fetch, url) {
        return fetchWithRetry(fetch, url).then((response) => response.text());
      }

    enableBlocking() { 
        this.enabled = true

        declarativeNetRequest.updateEnabledRulesets(
            {
                enableRulesetIds: [
                    "ruleset_1",
                    "ruleset_2",
                    "ruleset_3",
                    "ruleset_4"
                ]
            }
        )
        unblockListManager.initUnblockedList()
        this.setEngineEnabledLocal()
    }

    disableBlocking() { 
        this.enabled = false

        declarativeNetRequest.updateEnabledRulesets(
            {
                disableRulesetIds: [
                    "ruleset_1",
                    "ruleset_2",
                    "ruleset_3",
                    "ruleset_4"
                ]
            }
        )
        this.setEngineEnabledLocal()
    }

    isBlockingEnabled() { 
        return this.enabled
    }
    
    setEngineEnabledLocal() { 
        let jsonObj = {}
        jsonObj[this.engineName] = this.enabled
        storage.local.set(jsonObj)
    }

    setBlockingCallback(callback) { 
        this.blockingCallback = callback
    }

    store2Local(engineName) { 
        this.engineName = engineName
        var serializeData = this.serialize()
        return storage.local.set(engineName, {
            "engineData": serializeData.toString(),
            "enabled": this.enabled === undefined ? true : this.enabled
        })
    }

    setEngineName(engineName) { 
        this.engineName = engineName
    }

    
}

function fromWebRequestDetails(details) { 
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