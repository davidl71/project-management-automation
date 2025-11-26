var skipInt;
var speedUpAdInt;

var log = function (msg) {
    console.log(msg);
};
var skipAd = function () {
    var skipbtn = document.querySelector(".ytp-ad-skip-button.ytp-button") || document.querySelector(".videoAdUiSkipButton");
    if (skipbtn) {
        skipbtn = document.querySelector(".ytp-ad-skip-button.ytp-button") || document.querySelector(".videoAdUiSkipButton ");
        skipbtn.click();
        
        if (skipInt) {
            clearTimeout(skipInt);
        }
        skipInt = setTimeout(skipAd, 500);
    } else {
        if (skipInt) {
            clearTimeout(skipInt);
        }
        skipInt = setTimeout(skipAd, 500);
    }
};
skipAd();

// nativeParse = JSON.parse;

// function jsonPrune() {
//     var parseJson = function parseJson() {
//         for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
//             args[_key] = arguments[_key];
//         }
//         var origin = nativeParse.apply(window, args);
//         delete origin['adPlacements'];
//         delete origin['playerAds'];
//         delete origin['playerResponse.playerAds']
//         delete origin['playerResponse.adPlacements']
//         delete origin['0.playerResponse.playerAds']
//         delete origin['0.playerResponse.adPlacements']
//         return origin
//     };
//     JSON.parse = parseJson;
// }
// jsonPrune();

function setPropertyAccess(object, property, descriptor) {
    var currentDescriptor = Object.getOwnPropertyDescriptor(object, property);
    if (currentDescriptor && !currentDescriptor.configurable) {
        return false;
    }
    Object.defineProperty(object, property, descriptor);
    return true;
}

function setValue() {
    constantValue = undefined;
    descriptor = {
        get: function get() {
            return constantValue
        },
        set: function set(value) {
            constantValue = value
        },
        parseXML: function () {}
    };
    setPropertyAccess(Object.prototype, 'ytInitialPlayerResponse.adPlacements', descriptor);
    setPropertyAccess(Object.prototype, 'playerResponse.adPlacements', descriptor)
}
setValue();

(function () {
    try {
        var youtubeAdRegExp = /^((.*_)?(ad|ads|afv|adsense)(_.*)?|(ad3|st)_module|prerolls|interstitial|infringe|iv_cta_url)$/;

        function updateFlashvars(flashvars) {
            var values = flashvars.split('&');
            for (var i = 0; i < values.length; i++) {
                var param = values[i].split('=')[0];
                if (youtubeAdRegExp.test(param)) {
                    values.splice(i--, 1);
                }
            }
            return values.join('&');
        }

        function blockPlayerAds(player) {
            var updatedPlayer = player.cloneNode(true);
            var changed = false;
            var flashvars = updatedPlayer.getAttribute('flashvars');
            if (flashvars) {
                var flashvarsUpdated = updateFlashvars(flashvars);
                if (flashvars != flashvarsUpdated) {
                    updatedPlayer.setAttribute('flashvars', flashvarsUpdated);
                    changed = true;
                }
            }
            var param = updatedPlayer.querySelector('param[name=flashvars]');
            if (param) {
                var value = param.getAttribute('value');
                if (value) {
                    var valueUpdated = updateFlashvars(value);
                    if (value != valueUpdated) {
                        param.setAttribute('value', valueUpdated);
                        changed = true;
                    }
                }
            }
            if (changed && player.parentNode) {
                player.parentNode.replaceChild(updatedPlayer, player);
            }
            var container = document.querySelector(".video-ads");
            if (container && container.parentNode) {
                container.parentNode.removeChild(container);
            }
            var progress = document.querySelector(".html5-ad-progress-list");
            if (progress && progress.parentNode) {
                progress.parentNode.removeChild(progress);
            }
            if (typeof ytplayer == 'undefined') {
                return;
            }
            var config = ytplayer['config'];
            if (!config) {
                return;
            }
            config.loaded = false;
            var args = config['args'];
            if (!args) {
                return;
            }
            args.ad3_module = 0;
            args.ad_channel_code_instream = 0;
            args.ad_channel_code_overlay = 0;
            args.ad_device = 0;
            args.ad_eurl = 0;
            args.ad_host = 0;
            args.ad_host_tier = 0;
            args.ad_logging_flag = 0;
            args.ad_preroll = 0;
            args.ad_slots = 0;
            args.ad_tag = 0;
            args.ad_video_pub_id = 0;
            args.adsense_video_doc_id = 0;
            args.advideo = 0;
            args.afv = 0;
            args.afv_ad_tag = 0;
            args.afv_ad_tag_restricted_to_instream = 0;
            args.afv_instream_max = 0;
            args.allowed_ads = 0;
            args.afv_video_min_cpm = 0;
            args.allow_html5_ads = 0;
            args.excluded_ad = 0;
            args.dynamic_allocation_ad_tag = 0;
        }
        window.ytspf = {};
        Object.defineProperty(window.ytspf, 'enabled', {
            configurable: true,
            get: function () {
                return false;
            },
            set: function (enabled) {}
        });
        var player = document.querySelector('#movie_player');
        if (player) {
            blockPlayerAds(player);
        } else {
            let observerConfig = {
                characterData: false,
                subtree: true,
                childList: true,
                attributes: true,
                attributeFilter: ["id"]
            }
            var onMutationObserver = function (mutations) {
                mutations.forEach(mutation => {
                    if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                        const target = mutation.target.querySelector('#movie_player')
                        if (target) {
                            blockPlayerAds(target);
                            observer.disconnect();
                        }
                    } else if (mutation.target.id === 'movie_player') {
                        blockPlayerAds(mutation.target);
                        observer.disconnect();
                    }
                })
            }
        
            let observer = new MutationObserver(onMutationObserver)
            observer.observe(document, observerConfig)  
        }
    } catch (ex) {
        console.log('Youtube ads blocking error');
        console.log(ex);
    }
})();

var hasAds = false;
var speedupAds = function() {
    speedUpAdInt = setTimeout(speedupAds,1000)
    var adsSymbol = document.querySelector(".video-ads") || document.querySelector(".ytp-ad-module") 
    var adsShow = document.getElementsByClassName("ytp-ad-persistent-progress-bar-container")[0] != undefined && document.getElementsByClassName("ytp-ad-persistent-progress-bar-container")[0].style.display != "none";
    var adsShow2 = document.querySelector(".ad-showing") != undefined
    var video = document.getElementsByTagName("video")[0];
    if (adsShow || adsShow2) {
        hasAds = true
        document.getElementsByTagName("video")[0].playbackRate = 16;
        document.getElementsByTagName("video")[0].muted = true;
    }else{
        if(document.querySelector("#player-ads")){
            document.getElementById("player-ads").style.display = "none";
            hasAds = false
        }
        if (video){
            video.playbackRate = 1;
            video.muted = false;
        }
    }

    let skipBtn = document.querySelector(".ytp-skip-ad-button")
    if (skipBtn) {
        skipBtn.click()
    }
}
speedupAds();

console.log("youtube blocking script")


function jsonPrune(rawPrunePaths, rawNeedlePaths = "")
{
  if (!rawPrunePaths)
    throw new Error("Missing paths to prune");
  let prunePaths = rawPrunePaths.split(/ +/);
  let needlePaths = rawNeedlePaths !== "" ? rawNeedlePaths.split(/ +/) : [];
  let currentValue = JSON.parse;

  let descriptor = {
    value(...args)
    {
      let result;
      result = currentValue.apply(this, args);

      if (needlePaths.length > 0 &&
          needlePaths.some(path => !findOwner(result, path)))
        return result;

      for (let path of prunePaths)
      {
        let details = findOwner(result, path);
        if (typeof details != "undefined")
          delete details[0][details[1]];
      }
      return result;
    }
  };

  Object.defineProperty(JSON, "parse", descriptor);

    const isOwnProperty = Function.call.bind(Object.prototype.hasOwnProperty)
  function findOwner(root, path)
  {
    if (!(root instanceof window.Object))
      return;

    let object = root;
    let chain = path.split(".");

    if (chain.length === 0)
      return;

    for (let i = 0; i < chain.length - 1; i++)
    {
      let prop = chain[i];
      if (!isOwnProperty(object, prop))
        return;

      object = object[prop];

      if (!(object instanceof window.Object))
        return;
    }

    let prop = chain[chain.length - 1];
    if (isOwnProperty(object, prop))
      return [object, prop];
  }
}

jsonPrune('0.playerResponse.adPlacements 0.playerResponse.playerAds playerResponse.adPlacements playerResponse.playerAds adPlacements playerAds');