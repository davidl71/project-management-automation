let browser = chrome ? chrome : browser

function setL10N() { 
    $('.localize').each(function (index, item) {
        var localizeKey = $(item).data('localize');
        $(item).html(browser.i18n.getMessage(localizeKey));
    });
}
setL10N()