try {
    Object.defineProperty(document, 'visibilityState', {
        get() {
            return 'visible';
        }
    });
    Object.defineProperty(document, 'hidden', {
        get() {
            return false;
        }
    });
    const block = e => {
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
    };
    const process = e => {
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        //This corrects the background tab buffer bug when switching to the background tab for the first time after an extended period.
        doTwitchPlayerTask(false, false, true, false, false);
    };
    document.addEventListener('visibilitychange', process, true);
    document.addEventListener('webkitvisibilitychange', block, true);
    document.addEventListener('mozvisibilitychange', block, true);
    document.addEventListener('hasFocus', block, true);
    if (/Firefox/.test(navigator.userAgent)) {
        Object.defineProperty(document, 'mozHidden', {
            get() {
                return false;
            }
        });
    } else {
        Object.defineProperty(document, 'webkitHidden', {
            get() {
                return false;
            }
        });
    }
} catch (err) {}

//Send settings updates to worker.
window.addEventListener("message", (event) => {
    if (event.source != window)
        return;
    if (event.data.type && (event.data.type == "SetHideBlockingMessage")) {
        if (twitchMainWorker) {
            twitchMainWorker.postMessage({
                key: 'SetHideBlockingMessage',
                value: event.data.value
            });
        }
    }
}, false);

function declareOptions(scope) {
    scope.AdSignifier = 'stitched';
    scope.ClientID = 'kimne78kx3ncx6brgo4mv6wki5h1ko';
    scope.ClientVersion = 'null';
    scope.ClientSession = 'null';
    scope.PlayerType1 = 'site'; //Source
    scope.PlayerType2 = 'thunderdome'; //480p
    scope.PlayerType3 = 'pop_tart'; //480p
    scope.PlayerType4 = 'picture-by-picture'; //360p
    scope.CurrentChannelName = null;
    scope.UsherParams = null;
    scope.WasShowingAd = false;
    scope.GQLDeviceID = null;
    scope.HideBlockingMessage = false;
    scope.IsSquadStream = false;
}

declareOptions(window);

var twitchMainWorker = null;

var adBlockDiv = null;

var OriginalVideoPlayerQuality = null;

var IsPlayerAutoQuality = null;

const oldWorker = window.Worker;

window.Worker = class Worker extends oldWorker {
    constructor(twitchBlobUrl) {
        if (twitchMainWorker) {
            super(twitchBlobUrl);
            return;
        }
        var jsURL = getWasmWorkerUrl(twitchBlobUrl);
        if (typeof jsURL !== 'string') {
            super(twitchBlobUrl);
            return;
        }
        var newBlobStr = `
            ${getNewUsher.toString()}
            ${processM3U8.toString()}
            ${hookWorkerFetch.toString()}
            ${declareOptions.toString()}
            ${getAccessToken.toString()}
            ${gqlRequest.toString()}
            ${adRecordgqlPacket.toString()}
            ${tryNotifyTwitch.toString()}
            ${parseAttributes.toString()}
            declareOptions(self);
            self.addEventListener('message', function(e) {
                if (e.data.key == 'UpdateIsSquadStream') {
                    IsSquadStream = e.data.value;
                } else if (e.data.key == 'UpdateClientVersion') {
                    ClientVersion = e.data.value;
                } else if (e.data.key == 'UpdateClientSession') {
                    ClientSession = e.data.value;
                } else if (e.data.key == 'UpdateClientId') {
                    ClientID = e.data.value;
                } else if (e.data.key == 'UpdateDeviceId') {
                    GQLDeviceID = e.data.value;
                } else if (e.data.key == 'SetHideBlockingMessage') {
                    if (e.data.value == "true") {
                    HideBlockingMessage = false;
                    } else if (e.data.value == "false") {
                    HideBlockingMessage = true;
                    }
                }
            });
            hookWorkerFetch();
            importScripts('${jsURL}');
        `;
        super(URL.createObjectURL(new Blob([newBlobStr])));
        twitchMainWorker = this;
        this.onmessage = function(e) {
            if (e.data.key == 'ShowAdBlockBanner') {
                if (adBlockDiv == null) {
                    adBlockDiv = getAdBlockDiv();
                }
                adBlockDiv.P.textContent = 'Blocking ads...';
                adBlockDiv.style.display = 'block';
            } else if (e.data.key == 'HideAdBlockBanner') {
                if (adBlockDiv == null) {
                    adBlockDiv = getAdBlockDiv();
                }
                adBlockDiv.style.display = 'none';
            } else if (e.data.key == 'PauseResumePlayer') {
                doTwitchPlayerTask(true, false, false, false, false);
            } else if (e.data.key == 'ForceChangeQuality') {
                //This is used to fix the bug where the video would freeze.
                try {
                    var autoQuality = doTwitchPlayerTask(false, false, false, true, false);
                    var currentQuality = doTwitchPlayerTask(false, true, false, false, false);

                    if (IsPlayerAutoQuality == null) {
                        IsPlayerAutoQuality = autoQuality;
                    }
                    if (OriginalVideoPlayerQuality == null) {
                        OriginalVideoPlayerQuality = currentQuality;
                    }
                    if (!currentQuality.includes('480') || e.data.value != null) {
                        if (!OriginalVideoPlayerQuality.includes('480')) {
                            var settingsMenu = document.querySelector('div[data-a-target="player-settings-menu"]');
                            if (settingsMenu == null) {
                                var settingsCog = document.querySelector('button[data-a-target="player-settings-button"]');
                                if (settingsCog) {
                                    settingsCog.click();
                                    var qualityMenu = document.querySelector('button[data-a-target="player-settings-menu-item-quality"]');
                                    if (qualityMenu) {
                                        qualityMenu.click();
                                    }
                                    var lowQuality = document.querySelectorAll('input[data-a-target="tw-radio"');
                                    if (lowQuality) {
                                        var qualityToSelect = lowQuality.length - 3;
                                        if (e.data.value != null) {
                                            if (e.data.value.includes('original')) {
                                                e.data.value = OriginalVideoPlayerQuality;
                                                if (IsPlayerAutoQuality) {
                                                    e.data.value = 'auto';
                                                }
                                            }
                                            if (e.data.value.includes('160p')) {
                                                qualityToSelect = 5;
                                            }
                                            if (e.data.value.includes('360p')) {
                                                qualityToSelect = 4;
                                            }
                                            if (e.data.value.includes('480p')) {
                                                qualityToSelect = 3;
                                            }
                                            if (e.data.value.includes('720p')) {
                                                qualityToSelect = 2;
                                            }
                                            if (e.data.value.includes('822p')) {
                                                qualityToSelect = 2;
                                            }
                                            if (e.data.value.includes('864p')) {
                                                qualityToSelect = 2;
                                            }
                                            if (e.data.value.includes('900p')) {
                                                qualityToSelect = 2;
                                            }
                                            if (e.data.value.includes('936p')) {
                                                qualityToSelect = 2;
                                            }
                                            if (e.data.value.includes('960p')) {
                                                qualityToSelect = 2;
                                            }
                                            if (e.data.value.includes('1080p')) {
                                                qualityToSelect = 2;
                                            }
                                            if (e.data.value.includes('source')) {
                                                qualityToSelect = 1;
                                            }
                                            if (e.data.value.includes('auto')) {
                                                qualityToSelect = 0;
                                            }
                                        }
                                        var currentQualityLS = window.localStorage.getItem('video-quality');
                                        
                                        lowQuality[qualityToSelect].click();
                                        window.localStorage.setItem('video-quality', currentQualityLS);

                                        if (e.data.value != null) {
                                            OriginalVideoPlayerQuality = null;
                                            IsPlayerAutoQuality = null;
                                            doTwitchPlayerTask(false, false, false, true, true);
                                        }
                                    }

                                }
                            }
                        }
                    }
                } catch (err) {
                    OriginalVideoPlayerQuality = null;
                    IsPlayerAutoQuality = null;
                }
            }
        };

        function getAdBlockDiv() {
            //To display a notification to the user, that an ad is being blocked.
            var playerRootDiv = document.querySelector('.video-player');
            var adBlockDiv = null;
            if (playerRootDiv != null) {
                adBlockDiv = playerRootDiv.querySelector('.adblock-overlay');
                if (adBlockDiv == null) {
                    adBlockDiv = document.createElement('div');
                    adBlockDiv.className = 'adblock-overlay';
                    adBlockDiv.innerHTML = '<div class="player-adblock-notice" style="color: white; background-color: rgba(0, 0, 0, 0.8); position: absolute; top: 0px; left: 0px; padding: 5px;"><p></p></div>';
                    adBlockDiv.style.display = 'none';
                    adBlockDiv.P = adBlockDiv.querySelector('p');
                    playerRootDiv.appendChild(adBlockDiv);
                }
            }
            return adBlockDiv;
        }
    }
};

function getWasmWorkerUrl(twitchBlobUrl) {
    var req = new XMLHttpRequest();
    req.open('GET', twitchBlobUrl, false);
    req.send();
    return req.responseText.split("'")[1];
}

function hookWorkerFetch() {
    var realFetch = fetch;
    fetch = async function(url, options) {
        if (typeof url === 'string') {
            if (url.includes('video-weaver')) {
                return new Promise(function(resolve, reject) {
                    var processAfter = async function(response) {
                        //Here we check the m3u8 for any ads and also try fallback player types if needed.

                        var responseText = await response.text();
                        var weaverText = null;

                        weaverText = await processM3U8(url, responseText, realFetch, PlayerType2);
                        if (weaverText.includes(AdSignifier)) {
                            weaverText = await processM3U8(url, responseText, realFetch, PlayerType3);
                        }
                        if (weaverText.includes(AdSignifier)) {
                            weaverText = await processM3U8(url, responseText, realFetch, PlayerType4);
                        }

                        resolve(new Response(weaverText));
                    };
                    var send = function() {
                        return realFetch(url, options).then(function(response) {
                            processAfter(response);
                        })['catch'](function(err) {
                            reject(err);
                        });
                    };
                    send();
                });
            } else if (url.includes('/api/channel/hls/')) {
                var channelName = (new URL(url)).pathname.match(/([^\/]+)(?=\.\w+$)/)[0];
                UsherParams = (new URL(url)).search;
                CurrentChannelName = channelName;
                //To prevent pause/resume loop for mid-rolls.
                var isPBYPRequest = url.includes('picture-by-picture');
                if (isPBYPRequest) {
                    url = '';
                }
                //Make new Usher request if needed to create fallback if UBlock bypass method fails.
                var useNewUsher = false;
                if (url.includes('subscriber%22%3Afalse') && url.includes('hide_ads%22%3Afalse') && url.includes('show_ads%22%3Atrue')) {
                    useNewUsher = true;
                }
                if (url.includes('subscriber%22%3Atrue') && url.includes('hide_ads%22%3Afalse') && url.includes('show_ads%22%3Atrue')) {
                    useNewUsher = true;
                }
                if (useNewUsher == true) {
                    return new Promise(function(resolve, reject) {
                        var processAfter = async function(response) {
                            encodingsM3u8 = await getNewUsher(realFetch, response, channelName);
                            if (encodingsM3u8.length > 1) {
                                resolve(new Response(encodingsM3u8));
                            } else {
                                postMessage({
                                    key: 'HideAdBlockBanner'
                                });
                                resolve(encodingsM3u8);
                            }
                        };
                        var send = function() {
                            return realFetch(url, options).then(function(response) {
                                processAfter(response);
                            })['catch'](function(err) {
                                reject(err);
                            });
                        };
                        send();
                    });
                }
            }
        }
        return realFetch.apply(this, arguments);
    };
}

//Added as fallback for when UBlock method fails.
async function getNewUsher(realFetch, originalResponse, channelName) {
    var accessTokenResponse = await getAccessToken(channelName, PlayerType1);
    var encodingsM3u8 = '';

    if (accessTokenResponse.status === 200) {

        var accessToken = await accessTokenResponse.json();

        try {
            var urlInfo = new URL('https://usher.ttvnw.net/api/channel/hls/' + channelName + '.m3u8' + UsherParams);
            urlInfo.searchParams.set('sig', accessToken.data.streamPlaybackAccessToken.signature);
            urlInfo.searchParams.set('token', accessToken.data.streamPlaybackAccessToken.value);
            var encodingsM3u8Response = await realFetch(urlInfo.href);
            if (encodingsM3u8Response.status === 200) {
                encodingsM3u8 = await encodingsM3u8Response.text();
                return encodingsM3u8;
            } else {
                return originalResponse;
            }
        } catch (err) {}
        return originalResponse;
    } else {
        return originalResponse;
    }
}

async function processM3U8(url, textStr, realFetch, playerType) {
    //Checks the m3u8 for ads and if it finds one, instead returns an ad-free stream.

    //Ad blocking for squad streams is disabled due to the way multiple weaver urls are used. No workaround so far.
    if (IsSquadStream == true) {
        return textStr;
    }

    if (!textStr) {
        return textStr;
    }

    //Some live streams use mp4.
    if (!textStr.includes(".ts") && !textStr.includes(".mp4")) {
        return textStr;
    }

    var haveAdTags = textStr.includes(AdSignifier);

    if (haveAdTags) {

        //Reduces ad frequency.
        try {
            tryNotifyTwitch(textStr);
        } catch (err) {}

        var accessTokenResponse = await getAccessToken(CurrentChannelName, playerType);

        if (accessTokenResponse.status === 200) {

            var accessToken = await accessTokenResponse.json();

            try {
                var urlInfo = new URL('https://usher.ttvnw.net/api/channel/hls/' + CurrentChannelName + '.m3u8' + UsherParams);
                urlInfo.searchParams.set('sig', accessToken.data.streamPlaybackAccessToken.signature);
                urlInfo.searchParams.set('token', accessToken.data.streamPlaybackAccessToken.value);
                var encodingsM3u8Response = await realFetch(urlInfo.href);
                if (encodingsM3u8Response.status === 200) {

                    var encodingsM3u8 = await encodingsM3u8Response.text();

                    streamM3u8Url = encodingsM3u8.match(/^https:.*\.m3u8$/mg)[0];

                    var streamM3u8Response = await realFetch(streamM3u8Url);
                    if (streamM3u8Response.status == 200) {
                        var m3u8Text = await streamM3u8Response.text();
                        console.log("Blocking ads...");
                        WasShowingAd = true;
                        if (HideBlockingMessage == false) {
                            postMessage({
                                key: 'ShowAdBlockBanner'
                            });
                        } else if (HideBlockingMessage == true) {
                            postMessage({
                                key: 'HideAdBlockBanner'
                            });
                        }

                        postMessage({
                            key: 'ForceChangeQuality'
                        });

                        return m3u8Text;
                    } else {
                        return textStr;
                    }
                } else {
                    return textStr;
                }
            } catch (err) {}
            return textStr;
        } else {
            return textStr;
        }
    } else {
        if (WasShowingAd) {
            console.log("Done blocking ads, changing back to original quality");
            WasShowingAd = false;
            //Here we put player back to original quality and remove the blocking message.
            postMessage({
                key: 'ForceChangeQuality',
                value: 'original'
            });
            postMessage({
                key: 'PauseResumePlayer'
            });
            postMessage({
                key: 'HideAdBlockBanner'
            });
        }
        return textStr;
    }
    return textStr;
}

function parseAttributes(str) {
    return Object.fromEntries(
        str.split(/(?:^|,)((?:[^=]*)=(?:"[^"]*"|[^,]*))/)
        .filter(Boolean)
        .map(x => {
            const idx = x.indexOf('=');
            const key = x.substring(0, idx);
            const value = x.substring(idx + 1);
            const num = Number(value);
            return [key, Number.isNaN(num) ? value.startsWith('"') ? JSON.parse(value) : value : num];
        }));
}

async function tryNotifyTwitch(streamM3u8) {
    //We notify that an ad was requested but was not visible and was also muted.
    var matches = streamM3u8.match(/#EXT-X-DATERANGE:(ID="stitched-ad-[^\n]+)\n/);
    if (matches.length > 1) {
        const attrString = matches[1];
        const attr = parseAttributes(attrString);
        var podLength = parseInt(attr['X-TV-TWITCH-AD-POD-LENGTH'] ? attr['X-TV-TWITCH-AD-POD-LENGTH'] : '1');
        var podPosition = parseInt(attr['X-TV-TWITCH-AD-POD-POSITION'] ? attr['X-TV-TWITCH-AD-POD-POSITION'] : '0');
        var radToken = attr['X-TV-TWITCH-AD-RADS-TOKEN'];
        var lineItemId = attr['X-TV-TWITCH-AD-LINE-ITEM-ID'];
        var orderId = attr['X-TV-TWITCH-AD-ORDER-ID'];
        var creativeId = attr['X-TV-TWITCH-AD-CREATIVE-ID'];
        var adId = attr['X-TV-TWITCH-AD-ADVERTISER-ID'];
        var rollType = attr['X-TV-TWITCH-AD-ROLL-TYPE'].toLowerCase();
        const baseData = {
            stitched: true,
            roll_type: rollType,
            player_mute: true,
            player_volume: 0.0,
            visible: false,
        };
        for (let podPosition = 0; podPosition < podLength; podPosition++) {
            const extendedData = {
                ...baseData,
                ad_id: adId,
                ad_position: podPosition,
                duration: 0,
                creative_id: creativeId,
                total_ads: podLength,
                order_id: orderId,
                line_item_id: lineItemId,
            };
            await gqlRequest(adRecordgqlPacket('video_ad_impression', radToken, extendedData));
            for (let quartile = 0; quartile < 4; quartile++) {
                await gqlRequest(
                    adRecordgqlPacket('video_ad_quartile_complete', radToken, {
                        ...extendedData,
                        quartile: quartile + 1,
                    })
                );
            }
            await gqlRequest(adRecordgqlPacket('video_ad_pod_complete', radToken, baseData));
        }
    }
}

function adRecordgqlPacket(event, radToken, payload) {
    return [{
        operationName: 'ClientSideAdEventHandling_RecordAdEvent',
        variables: {
            input: {
                eventName: event,
                eventPayload: JSON.stringify(payload),
                radToken,
            },
        },
        extensions: {
            persistedQuery: {
                version: 1,
                sha256Hash: '7e6c69e6eb59f8ccb97ab73686f3d8b7d85a72a0298745ccd8bfc68e4054ca5b',
            },
        },
    }];
}

function getAccessToken(channelName, playerType, realFetch) {
    var body = null;
    var templateQuery = 'query PlaybackAccessToken_Template($login: String!, $isLive: Boolean!, $vodID: ID!, $isVod: Boolean!, $playerType: String!) {  streamPlaybackAccessToken(channelName: $login, params: {platform: "web", playerBackend: "mediaplayer", playerType: $playerType}) @include(if: $isLive) {    value    signature    __typename  }  videoPlaybackAccessToken(id: $vodID, params: {platform: "web", playerBackend: "mediaplayer", playerType: $playerType}) @include(if: $isVod) {    value    signature    __typename  }}';
    body = {
        operationName: 'PlaybackAccessToken_Template',
        query: templateQuery,
        variables: {
            'isLive': true,
            'login': channelName,
            'isVod': false,
            'vodID': '',
            'playerType': playerType
        }
    };
    return gqlRequest(body, realFetch);
}

function gqlRequest(body, realFetch) {
    var fetchFunc = realFetch ? realFetch : fetch;
    if (!GQLDeviceID) {
        var dcharacters = 'abcdefghijklmnopqrstuvwxyz0123456789';
        var dcharactersLength = dcharacters.length;
        for (var i = 0; i < 32; i++) {
            GQLDeviceID += dcharacters.charAt(Math.floor(Math.random() * dcharactersLength));
        }
    }
    return fetchFunc('https://gql.twitch.tv/gql', {
        method: 'POST',
        body: JSON.stringify(body),
        headers: {
            'Client-ID': ClientID,
            'Device-ID': GQLDeviceID,
            'X-Device-Id': GQLDeviceID,
            'Client-Version': ClientVersion,
            'Client-Session-Id': ClientSession
        }
    });
}

function doTwitchPlayerTask(isPausePlay, isCheckQuality, isCorrectBuffer, isAutoQuality, setAutoQuality) {
    //This will do an instant pause/play to return to original quality once the ad is finished.
    //We also use this function to get the current video player quality set by the user.
    //We also use this function to quickly pause/play the player when switching tabs to stop delays.
    try {
        var videoController = null;
        var videoPlayer = null;

        function findReactNode(root, constraint) {
            if (root.stateNode && constraint(root.stateNode)) {
                return root.stateNode;
            }
            let node = root.child;
            while (node) {
                const result = findReactNode(node, constraint);
                if (result) {
                    return result;
                }
                node = node.sibling;
            }
            return null;
        }
        var reactRootNode = null;
        var rootNode = document.querySelector('#root');
        if (rootNode && rootNode._reactRootContainer && rootNode._reactRootContainer._internalRoot && rootNode._reactRootContainer._internalRoot.current) {
            reactRootNode = rootNode._reactRootContainer._internalRoot.current;
        }
        videoPlayer = findReactNode(reactRootNode, node => node.setPlayerActive && node.props && node.props.mediaPlayerInstance);
        videoPlayer = videoPlayer && videoPlayer.props && videoPlayer.props.mediaPlayerInstance ? videoPlayer.props.mediaPlayerInstance : null;

        if (isPausePlay) {
            videoPlayer.pause();
            videoPlayer.play();
            return;
        }
        if (isCheckQuality) {
            if (typeof videoPlayer.getQuality() == 'undefined') {
                return;
            }
            var playerQuality = JSON.stringify(videoPlayer.getQuality());
            if (playerQuality) {
                return playerQuality;
            } else {
                return;
            }
        }
        if (isAutoQuality) {
            if (typeof videoPlayer.isAutoQualityMode() == 'undefined') {
                return false;
            }
            var autoQuality = videoPlayer.isAutoQualityMode();
            if (autoQuality) {
                videoPlayer.setAutoQualityMode(false);
                return autoQuality;
            } else {
                return false;
            }
        }
        if (setAutoQuality) {
            videoPlayer.setAutoQualityMode(true);
            return;
        }
        //This only happens when switching tabs and is to correct the high latency caused when opening background tabs and going to them at a later time.
        //We check that this is a live stream by the page URL, to prevent vod/clip pause/plays.
        try {
            var currentPageURL = document.URL;
            var isLive = true;
            if (currentPageURL.includes('videos/') || currentPageURL.includes('clip/')) {
                isLive = false;
            }
            if (isCorrectBuffer && isLive) {
                //A timer is needed due to the player not resuming without it.
                setTimeout(function() {
                    //If latency to broadcaster is above 5 or 15 seconds upon switching tabs, we pause and play the player to reset the latency.
                    //If latency is between 0-6, user can manually pause and resume to reset latency further.
                    if (videoPlayer.isLiveLowLatency() && videoPlayer.getLiveLatency() > 5) {
                        videoPlayer.pause();
                        videoPlayer.play();
                    } else if (videoPlayer.getLiveLatency() > 15) {
                        videoPlayer.pause();
                        videoPlayer.play();
                    }
                }, 3000);
            }
        } catch (err) {}
    } catch (err) {}
}

var localDeviceID = null;
localDeviceID = window.localStorage.getItem('local_copy_unique_id');

function hookFetch() {
    console.log("twitch block script")
    var realFetch = window.fetch;
    window.fetch = function(url, init, ...args) {
        if (typeof url === 'string') {
            //Check if squad stream.
            if (window.location.pathname.includes('/squad')) {
                if (twitchMainWorker) {
                    twitchMainWorker.postMessage({
                        key: 'UpdateIsSquadStream',
                        value: true
                    });
                }
            } else {
                if (twitchMainWorker) {
                    twitchMainWorker.postMessage({
                        key: 'UpdateIsSquadStream',
                        value: false
                    });
                }
            }
            if (url.includes('/access_token') || url.includes('gql')) {
                //Device ID is used when notifying Twitch of ads.
                var deviceId = init.headers['X-Device-Id'];
                if (typeof deviceId !== 'string') {
                    deviceId = init.headers['Device-ID'];
                }
                //Added to prevent eventual UBlock conflicts.
                if (typeof deviceId === 'string' && !deviceId.includes('twitch-web-wall-mason')) {
                    GQLDeviceID = deviceId;
                } else if (localDeviceID) {
                    GQLDeviceID = localDeviceID.replace('"', '');
                    GQLDeviceID = GQLDeviceID.replace('"', '');
                }
                if (GQLDeviceID && twitchMainWorker) {
                    if (typeof init.headers['X-Device-Id'] === 'string') {
                        init.headers['X-Device-Id'] = GQLDeviceID;
                    }
                    if (typeof init.headers['Device-ID'] === 'string') {
                        init.headers['Device-ID'] = GQLDeviceID;
                    }
                    twitchMainWorker.postMessage({
                        key: 'UpdateDeviceId',
                        value: GQLDeviceID
                    });
                }
                //Client version is used in GQL requests.
                var clientVersion = init.headers['Client-Version'];
                if (clientVersion && typeof clientVersion == 'string') {
                    ClientVersion = clientVersion;
                }
                if (ClientVersion && twitchMainWorker) {
                    twitchMainWorker.postMessage({
                        key: 'UpdateClientVersion',
                        value: ClientVersion
                    });
                }
                //Client session is used in GQL requests.
                var clientSession = init.headers['Client-Session-Id'];
                if (clientSession && typeof clientSession == 'string') {
                    ClientSession = clientSession;
                }
                if (ClientSession && twitchMainWorker) {
                    twitchMainWorker.postMessage({
                        key: 'UpdateClientSession',
                        value: ClientSession
                    });
                }
                //Client ID is used in GQL requests.
                if (url.includes('gql') && init && typeof init.body === 'string' && init.body.includes('PlaybackAccessToken')) {
                    var clientId = init.headers['Client-ID'];
                    if (clientId && typeof clientId == 'string') {
                        ClientID = clientId;
                    } else {
                        clientId = init.headers['Client-Id'];
                        if (clientId && typeof clientId == 'string') {
                            ClientID = clientId;
                        }
                    }
                    if (ClientID && twitchMainWorker) {
                        twitchMainWorker.postMessage({
                            key: 'UpdateClientId',
                            value: ClientID
                        });
                    }
                }
                //To prevent pause/resume loop for mid-rolls.
                if (url.includes('gql') && init && typeof init.body === 'string' && init.body.includes('PlaybackAccessToken') && init.body.includes('picture-by-picture')) {
                    init.body = '';
                }
                var isPBYPRequest = url.includes('picture-by-picture');
                if (isPBYPRequest) {
                    url = '';
                }
            }
        }
        return realFetch.apply(this, arguments);
    };
}
hookFetch();

(function () {
    console.log("twitch block script 2")
    var _tmuteVars = {
        "timerCheck": 1000, // Checking rate of ad in progress (in ms ; EDITABLE)
        "playerMuted": false, // Player muted or not (due to ad in progress)
        "adsDisplayed": 0, // Number of ads displayed
        "disableDisplay": true, // Disable the player display during an ad (true = yes, false = no (default) ; EDITABLE)
        "alreadyMuted": false, // Used to check if the player is muted at the start of an ad
        "adElapsedTime": undefined, // Used to check if Twitch forgot to remove the ad notice
        "adUnlockAt": 210, // Unlock the player if this amount of seconds elapsed during an ad (EDITABLE)
        "adMinTime": 7, // Minimum amount of seconds the player will be muted/hidden since an ad started (EDITABLE)
        "squadPage": false, // Either the current page is a squad page or not
        "playerIdAds": 0, // Player ID where ads may be displayed (default 0, varying on squads page)
        "displayingOptions": false, // Either ads options are currently displayed or not
        "highwindPlayer": undefined, // If you've the Highwind Player or not
        "classFallback": false, // If we're in a browser without the main ad notice class
        "currentPage": undefined // Current page to know if we need to reset ad detection on init
    };

    // Selectors for the old player and the highwind one
    var _tmuteSelectors = {
        "old": {
            "player": "player-video", // Player class
            "playerVideo": ".player-video", // Player video selector
            "muteButton": ".player-button--volume", // (un)mute button selector
            "adNotice": "player-ad-notice", // Ad notice class
            "adNoticeFallback": "player-ad-notice", // Ad notice fallback class as the main one seems missing in at least Chrome
            "viewersCount": "channel-info-bar__viewers-wrapper", // Viewers count wrapper class
            "squadHeader": "squad-stream-top-bar__container", // Squad bar container class
            "squadPlayer": "multi-stream-player-layout__player-container", // Squad player class
            "squadPlayerMain": "multi-stream-player-layout__player-primary" // Squad primary player class
        },
        "hw": {
            "player": "video-player__container", // Player class
            "playerVideo": ".video-player__container video", // Player video selector
            "muteButton": "button[data-a-target='player-mute-unmute-button']", // (un)mute button selector
            "adNotice": "Layout-sc-nxg1ff-0 fpnJwy", // Ad notice class
            "adNoticeFallback": "fpnJwy", // Ad notice fallback class as the main one seems missing in at least Chrome
            "viewersCount": "metadata-layout__support", // Viewers count wrapper class
            "squadHeader": "squad-stream-top-bar__container", // Squad bar container class
            "squadPlayer": "multi-stream-player-layout__player-container", // Squad player class
            "squadPlayerMain": "multi-stream-player-layout__player-primary" // Squad primary player class
        }
    };
    // Current selector (either old or highwind player, automatically set below)
    var currentSelector = undefined;

    // Check if there's an ad
    function checkAd() {
        // Check if you're watching a stream, useless to continue if not
        if (_tmuteVars.highwindPlayer === undefined) {
            var isOldPlayer = document.getElementsByClassName(_tmuteSelectors.old.player).length;
            var isHwPlayer = document.getElementsByClassName(_tmuteSelectors.hw.player).length;
            var isViewing = Boolean(isOldPlayer + isHwPlayer);
            if (isViewing === false) return;

            // We set the type of player currently used (old or highwind one)
            _tmuteVars.highwindPlayer = Boolean(isHwPlayer);
            currentSelector = (_tmuteVars.highwindPlayer === true) ? _tmuteSelectors.hw : _tmuteSelectors.old;
            console.log("You're currently using the " + ((_tmuteVars.highwindPlayer === true) ? "Highwind" : "old") + " player.");
        } else {
            var isViewing = Boolean(document.getElementsByClassName(currentSelector.player).length);
            if (isViewing === false) return;
        }

        // Initialize the ads options if necessary.
        var optionsInitialized = (document.getElementById("_tmads_options") === null) ? false : true;
        if (optionsInitialized === false) adsOptions("init");

        var selectorId = _tmuteVars.playerIdAds * 2;
        var advert = document.getElementsByClassName(currentSelector.adNotice)[selectorId];
        if (advert === undefined) { 
            return
        }
        if (_tmuteVars.adElapsedTime !== undefined) {
            _tmuteVars.adElapsedTime += _tmuteVars.timerCheck / 1000;
            if (_tmuteVars.adElapsedTime >= _tmuteVars.adUnlockAt && advert.childNodes[1] !== undefined) {
                for (var i = 0; i < advert.childElementCount; i++) {
                    if (!advert.childNodes[i].classList.contains(currentSelector.adNotice)) advert.removeChild(advert.childNodes[i]);
                }
                console.log("Unlocking Twitch player as Twitch forgot to remove the ad notice after the ad(s).");
            }
        }

        if ((advert.childElementCount > 2 && _tmuteVars.playerMuted === false) || (_tmuteVars.playerMuted === true && advert.childElementCount <= 2)) {
            // Update at the start of an ad if the player is already muted or not
            if (advert.childElementCount > 2) {
                var muteButton = document.querySelectorAll(currentSelector.muteButton)[_tmuteVars.playerIdAds];
                if (_tmuteVars.highwindPlayer === true) {
                    _tmuteVars.alreadyMuted = Boolean(muteButton.getAttribute("aria-label") === "Unmute (m)");
                } else {
                    _tmuteVars.alreadyMuted = Boolean(muteButton.childNodes[0].className === "unmute-button");
                }
            }

            // Keep the player muted/hidden for the minimum ad time set (Twitch started to remove the ad notice before the end of some ads)
            if (advert.childElementCount <= 2 && _tmuteVars.adElapsedTime !== undefined && _tmuteVars.adElapsedTime < _tmuteVars.adMinTime) return;

            mutePlayer();
        }
    }

    // (un)Mute Player
    function mutePlayer() {
        if (document.querySelectorAll(currentSelector.muteButton).length >= 1) {
            if (_tmuteVars.alreadyMuted === false) document.querySelectorAll(currentSelector.muteButton)[_tmuteVars.playerIdAds].click(); // If the player is already muted before an ad, we avoid to unmute it.
            _tmuteVars.playerMuted = !(_tmuteVars.playerMuted);

            if (_tmuteVars.playerMuted === true) {
                _tmuteVars.adsDisplayed++;
                _tmuteVars.adElapsedTime = 1;
                console.log("Ad #" + _tmuteVars.adsDisplayed + " detected. Player " + (_tmuteVars.alreadyMuted === true ? "already " : "") + "muted.");
                if (_tmuteVars.disableDisplay === true) document.querySelectorAll(currentSelector.playerVideo)[_tmuteVars.playerIdAds].style.visibility = "hidden";
            } else {
                console.log("Ad #" + _tmuteVars.adsDisplayed + " finished (lasted " + _tmuteVars.adElapsedTime + "s)." + (_tmuteVars.alreadyMuted === true ? "" : " Player unmuted."));
                _tmuteVars.adElapsedTime = undefined;
                if (_tmuteVars.disableDisplay === true) document.querySelectorAll(currentSelector.playerVideo)[_tmuteVars.playerIdAds].style.visibility = "visible";
            }
        } else {
            console.log("No volume button found (class changed ?).");
        }
    }

    // Manage ads options
    function adsOptions(changeType = "show") {
        switch (changeType) {
            // Manage player display during an ad (either hiding the ads or still showing them)
            case "display":
                _tmuteVars.disableDisplay = !(_tmuteVars.disableDisplay);
                // Update the player display if an ad is supposedly in progress
                if (_tmuteVars.playerMuted === true) document.querySelectorAll(currentSelector.playerVideo)[_tmuteVars.playerIdAds].style.visibility = (_tmuteVars.disableDisplay === true) ? "hidden" : "visible";
                document.getElementById("_tmads_display").innerText = (_tmuteVars.disableDisplay === true ? "Show" : "Hide") + " player during ads";
                break;
                // Force a player unlock if Twitch didn't remove the ad notice properly instead of waiting the auto unlock
            case "unlock":
                var advert = document.getElementsByClassName(currentSelector.adNotice)[0];

                if (_tmuteVars.adElapsedTime === undefined && advert.childNodes[1] === undefined) {
                    alert("There's no ad notice displayed. No unlock to do.");
                } else {
                    // We set the elapsed time to the unlock timer to trigger it during the next check.
                    _tmuteVars.adElapsedTime = _tmuteVars.adUnlockAt;
                    console.log("Unlock requested.");
                }
                break;
                // Display the ads options button
            case "init":
                // Do the resets needed if we changed page during an ad
                if (_tmuteVars.playerMuted === true && window.location.pathname != _tmuteVars.currentPage) {
                    mutePlayer();
                }
                _tmuteVars.currentPage = window.location.pathname;

                if (document.getElementsByClassName(currentSelector.viewersCount)[0] === undefined && document.getElementsByClassName(currentSelector.squadHeader)[0] === undefined) break;

                // Check ad notice class exists, otherwise we'll use the fallback class
                if (document.getElementsByClassName(currentSelector.adNotice)[0] === undefined) {
                    _tmuteVars.classFallback = true;
                    currentSelector.adNotice = currentSelector.adNoticeFallback;
                    console.log("Main ad notice class not found, falling back on another one.");

                    // If the fallback isn't found either, we try a last thing or we stop the script as Twitch did further changes that require a script update
                    if (document.getElementsByClassName(currentSelector.adNotice)[0] === undefined) {
                        clearInterval(_tmuteVars.autoCheck); // Temporarily stop the checks while we do a last search on a specific element that could still find the ad notice class
                        console.log("Trying to retrieve the new ad notice class, 1st fallback one wasn't found, Twitch changed something. Feel free to contact the author of the script.");
                        var lastFallback = document.querySelector("[data-a-target='ax-overlay']");

                        // We found the new ad notice class, restarting the checks
                        if (lastFallback !== null) {
                            _tmuteVars.classFallback = true;
                            currentSelector.adNotice = lastFallback.parentNode.className;
                            console.log("New ad notice class retrieved (\"" + currentSelector.adNotice + "\") and set as new fallback.");
                            _tmuteVars.autoCheck = setInterval(checkAd, _tmuteVars.timerCheck);
                        } else {
                            console.log("Script stopped. Last fallback ad notice class not found either, Twitch changed something. Feel free to contact the author of the script.");
                        }
                    }
                }

                // Append ads options and events related
                var optionsTemplate = document.createElement("div");
                optionsTemplate.id = "_tmads_options-wrapper";
                optionsTemplate.className = "tw-inline-flex";
                optionsTemplate.style = "padding-top: 10px;";
                optionsTemplate.innerHTML = `
          <span id="_tmads_options" style="display: none;">
            <button type="button" id="_tmads_unlock" style="padding: 0 2px 0 2px; margin-left: 2px; height: 16px; width: unset;" class="tw-interactive tw-button-icon tw-button-icon--hollow">Unlock player</button>
            <button type="button" id="_tmads_display" style="padding: 0 2px 0 2px; margin-left: 2px; height: 16px; width: unset;" class="tw-interactive tw-button-icon tw-button-icon--hollow">` + (_tmuteVars.disableDisplay === true ? "Show" : "Hide") + ` player during ads</button>
          </span>
          <button type="button" id="_tmads_showoptions" style="padding: 0 2px 0 2px; margin-left: 2px; height: 16px; width: unset;" class="tw-interactive tw-button-icon tw-button-icon--hollow">Ads Options</button>`;

                // Normal player page
                if (document.getElementsByClassName(currentSelector.viewersCount)[0] !== undefined) {
                    _tmuteVars.squadPage = false;
                    _tmuteVars.playerIdAds = 0;
                    document.getElementsByClassName(currentSelector.viewersCount)[0].parentNode.childNodes[1].appendChild(optionsTemplate);
                    // Squad page
                } else if (document.getElementsByClassName(currentSelector.squadHeader)[0] !== undefined) {
                    _tmuteVars.squadPage = true;
                    _tmuteVars.playerIdAds = 0;
                    // Since the primary player is never at the same place, we've to find it.
                    for (var i = 0; i < parseInt(document.querySelectorAll(currentSelector.playerVideo).length); i++) {
                        if (document.getElementsByClassName(currentSelector.squadPlayer)[0].childNodes[i].classList.contains(currentSelector.squadPlayerMain)) {
                            _tmuteVars.playerIdAds = i;
                            break;
                        }
                    }
                    document.getElementsByClassName(currentSelector.squadHeader)[0].appendChild(optionsTemplate);
                }

                document.getElementById("_tmads_showoptions").addEventListener("click", adsOptions, false);
                document.getElementById("_tmads_display").addEventListener("click", function () {
                    adsOptions("display");
                }, false);
                document.getElementById("_tmads_unlock").addEventListener("click", function () {
                    adsOptions("unlock");
                }, false);
                console.log("Ads options initialized.");

                break;
                // Display/Hide the ads options
            case "show":
            default:
                _tmuteVars.displayingOptions = !(_tmuteVars.displayingOptions);
                document.getElementById("_tmads_options").style.display = (_tmuteVars.displayingOptions === false) ? "none" : "inline-flex";
        }
    }

    // Start the background check
    _tmuteVars.autoCheck = setInterval(checkAd, _tmuteVars.timerCheck);
    console.log("add js")
})();