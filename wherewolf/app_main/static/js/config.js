/*
    Defines a global config object
    Allows client side interaction with objects set in Django templates
 */
define(["config-util"], function (configUtil) {

    // window.config should have been populated in django template
    if (!window.config) {
        window.config = {};
    }

    // create global config object
    var props = {

    };

    // mix into window.config
    $.extend(window.config, props);
    return window.config;

});
