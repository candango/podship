$(function(){
    var option = {
        fallbackLng: false, lng: 'en',
        resGetPath: '/locales/__lng__.json'
    }
    i18n.init(option, function(t) {
        // translate nav
        $('.login').i18n();
    });
});
