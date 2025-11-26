document.getElementById('agree').addEventListener("click", jump);
document.getElementById('license').addEventListener("click", jumpToLicensePage);
document.getElementById('privacy').addEventListener("click", jumpToPrivacyPage);
document.getElementById('dcn').addEventListener("click", jumpToDCNPage);
let browser = chrome ? chrome : browser

function jump() {
    
    browser.runtime.sendMessage({
        "cmd":"AccecptGDPR"
    }, (response) => {
        if (response === "true") { 
            window.location.href = "tutorial.html";
        }
    })
}

function jumpToLicensePage() {
   window.open("http://gr.trendmicro.com/GREntry/NonPayment?Target=AdBlockOneChrome&OS=&SP=&PID=CABO10&FunID=LicenseAgreement&VID=&Locale=EN-US");
}

function jumpToPrivacyPage() {
    window.open("http://gr.trendmicro.com/GREntry/NonPayment?Target=AdBlockOneChrome&OS=&SP=&PID=CABO10&FunID=PrivacyPolicy&VID=&Locale=EN-US");
}

function jumpToDCNPage() {
    window.open("http://gr.trendmicro.com/GREntry/NonPayment?Target=AdBlockOneChrome&OS=&SP=&PID=CABO10&FunID=DataCollectionNotice&VID=&Locale=EN-US");
}

function setL10N() { 
    $('.localize').each(function (index, item) {
        var localizeKey = $(item).data('localize');
        $(item).html(browser.i18n.getMessage(localizeKey));
    });
}
setL10N()