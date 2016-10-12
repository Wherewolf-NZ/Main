define([], function () {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function addCsrfTokenToDataObject(data) {
        var csrfToken = getCookie('csrftoken');
        data['csrfmiddlewaretoken'] = csrfToken;

    }

    function getUrlParamsDictionary(url) {

        var urlParamDict = {};

        // split url and get a dict of params
        var split = url.split('?');
        if (split.length > 1) {
            var paramsStr = split[1];
            var paramsStrSplit = paramsStr.split("&");
            for (var i = 0; i < paramsStrSplit.length; i++) {
                var p1 = paramsStrSplit[i].split('=')[0];
                var p2 = paramsStrSplit[i].split('=')[1];
                urlParamDict[p1] = p2;
            }
        }

        return urlParamDict;

    }

    function getUrlParam(url, paramKey) {
        var paramDict = getUrlParamsDictionary(url);

        if (paramKey in paramDict) {
            return paramDict[paramKey];
        }
        return null;

    }

    function removeUrlParam(url, paramKey) {
        var split = url.split('?');
        var urlPart1 = split[0];

        var urlParamDict = getUrlParamsDictionary(url);
        if (paramKey in urlParamDict) {
            delete urlParamDict[paramKey];
        }

        // convert to new url
        return urlParamsToUrlString(urlPart1, urlParamDict);
    }

    function addUrlParam(url, paramKey, paramValue) {
        var split = url.split('?');
        var urlPart1 = split[0];

        var urlParamDict = getUrlParamsDictionary(url);
        urlParamDict[paramKey] = paramValue;

        // convert to new url
        return urlParamsToUrlString(urlPart1, urlParamDict);
    }

    function getUrlPart(url, afterParam) {

        if (!url) {
            url = location.href;
        }

        urlParts = url.split("/");
        var foundPartIndex = -1;
        for (var a = 0; a < urlParts.length; a++) {
            var part = urlParts[a];
            if (part.toLowerCase() === afterParam.toLowerCase()) {
                foundPartIndex = a + 1;
                break;
            }
        }
        if (foundPartIndex > -1 && foundPartIndex < urlParts.length) {
            return urlParts[foundPartIndex];
        }
        return null;
    }

    function urlParamsToUrlString(urlPart1, urlParamDict) {

        if (Object.keys(urlParamDict).length === 0) {
            return urlPart1;
        }

        var newUrl = urlPart1 + "?";
        var c = 0;
        for (key in urlParamDict) {
            if (c > 0) {
                newUrl += "&"
            }
            newUrl += key + "=" + urlParamDict[key];
            c++;
        }
        return newUrl;
    }


    function getPage(pathIndex) {

        var index = pathIndex + 1;
        var page = $(location).attr('pathname'); // Example: "/feature/all/"
        var pagePaths = page.split("/");

        if (pagePaths.length > index)
        {
            return pagePaths[index];
        }
        return null;

    }


    return {
        addUrlParam: addUrlParam,
        getUrlParam: getUrlParam,
        removeUrlParam: removeUrlParam,
        getUrlPart: getUrlPart,
        getCookie: getCookie,
        addCsrfTokenToDataObject: addCsrfTokenToDataObject,
        getPage: getPage

    }


});
