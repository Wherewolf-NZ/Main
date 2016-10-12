/*
 main JS file, loaded by require.js
 */

require.config({
    baseUrl: '/static/js',
    paths: {
        // the left side is the module ID,
        // the right side is the path to
        // the jQuery file, relative to baseUrl.
        //jquery: 'jquery'
        jquery: '/static/js/lib/jquery'
    }
});

require(["config"],
    function (config) {

        window.config = config;

        /* global events
        example usage:

            // send event
            $(GlobalEvent).trigger(GlobalEvent.EVENT_FEATURE_CLiCK, [this.feature])
            // listen
            $(GlobalEvent).bind(GlobalEvent.EVENT_FEATURE_CLiCK, myFunction);

        */
        window.GlobalEvent = {
            EVENT_FEATURE_CLICK: "globalEventFeatureClick",
        };

        $(document).ready(function () {


        });

    });
