(function () {
    var factory = function (exports) {
        var $ = jQuery;
        var cm;
        var cachekey = (location.protocol + location.host + location.pathname + location.search).replace(/[.:?=\/-]/g, '_');

        exports.AutoSave = function () {

        };

        exports.fn.CodeAutoSave = function () {
            var settings = this.settings;

            if (typeof (Storage) == 'undefined') {
                console.warn('很遗憾,你的浏览器不支持Web存储.');
                return;
            }

            if (typeof settings.onautosave == 'function') {
                this.cm.on('change', settings.onautosave);
            }
        };

        exports.fn.CodeAutoSaveSetCache = function (data) {
            if (data) {
                var settings = this.settings;
                localStorage.setItem(settings.cachekey || cachekey, JSON.stringify(data));
            }
        }

        exports.fn.CodeAutoSaveGetCache = function () {
            var settings = this.settings;
            var data = localStorage.getItem(settings.cachekey || cachekey);
            return JSON.parse(data);
        }

        exports.fn.CodeAutoSaveRemoveCache = function(){
            var settings = this.settings;
            localStorage.removeItem(settings.cachekey || cachekey);
        }
    };

    if (typeof require === 'function' && typeof exports === 'object' && typeof module === 'object') {
        module.exports = factory;
    } else if (typeof define === 'function') {
        if (define.amd) {
            // for Require.js
            define(["editormd"], function (editormd) {
                factory(editormd);
            });
        } else {
            // for Sea.js
            define(function (require) {
                var editormd = require("./../../editormd");
                factory(editormd);
            });
        }
    } else {
        factory(window.editormd);
    }
})();