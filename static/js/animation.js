var SlrAnimation = function (homeName) {
    this.x = 0;
    this.y = 0;
    this.geo = {};
    this.name = homeName;
    this.putGeo(homeName, 0, 0);
};

SlrAnimation.prototype = {

    fade: {
        'in': function ($rootEl, order) {
            var selector = '.in'+order+'-fade';
            var $animated = $rootEl.find(selector);
            if ($animated.length === 0) {
                return promiseUnit();
            }
            var deferred = new $.Deferred();
            $animated.velocity({opacity: '1.0'}, {
                duration: 'slow',
                complete: function () { deferred.resolve(); }
            });
            return deferred.promise();
        },
        'out': function ($rootEl, order) {
            var selector = '.out'+order+'-fade';
            var $animated = $rootEl.find(selector);
            if ($animated.length === 0) {
                return promiseUnit();
            }
            var deferred = new $.Deferred();
            $animated.velocity({opacity: '0.0'}, {
                duration: 'slow',
                complete: function () { deferred.resolve(); }
            });
            return deferred.promise();
        }
    },

    bounce: {
        'in': function ($rootEl, order) {
            var selector = '.in'+order+'-bounce';
            var $animated = $rootEl.find(selector);
            if ($animated.length === 0) {
                return promiseUnit();
            }
            var deferred = new $.Deferred();
            $animated.velocity('callout.bounce', {
                complete: function () { deferred.resolve(); }
            });
            return deferred.promise();
        },
        'out': function ($rootEl, order) {
            var selector = '.out'+order+'-bounce';
            var $animated = $rootEl.find(selector);
            if ($animated.length === 0) {
                return promiseUnit();
            }
            var deferred = new $.Deferred();
            $animated.velocity('callout.bounce', {
                complete: function () { deferred.resolve(); }
            });
            return deferred.promise();
        }
    },

    animateInOut: function ($rootEl, type) {
        var self = this;
        var continuations = new Array();
        [1, 2, 3, 4, 5, 6, 7, 8, 9].forEach(function (i) {
            continuations.push(function () {
                var deferred = new $.Deferred();
                var count = 2;
                var resolveOnCount = function () {
                    --count;
                    if (count == 0) {
                        deferred.resolve();
                    }
                };
                self.fade[type]($rootEl, i).then(resolveOnCount);
                self.bounce[type]($rootEl, i).then(resolveOnCount);
                return deferred.promise();
            });
        });
        return promisePipe(promiseUnit(), continuations);
    },

    animateIn: function ($rootEl) {
        return this.animateInOut($rootEl, 'in');
    },

    animateOut: function ($rootEl) {
        return this.animateInOut($rootEl, 'out');
    },


    putGeo: function (name, screensX, screensY) {
        this.geo[name] = [screensX, screensY];
    },

    moveTo: function (name) {
        var self = this;
        if (this.geo.hasOwnProperty(name)) {
            var screensX = this.geo[name][0];
            var screensY = this.geo[name][1];
            var destX = screensX * $(window).width();
            var destY = screensY * $(window).height();
            var deltaX = destX - this.x;
            var deltaY = destY - this.y;
            return promisePipe(this.animateOut($(this.name)), [
                    function () {
                        return $('.screenful').animate({
                            left: '+='+deltaX,
                            top: '+='+deltaY
                        }, 'slow').promise();
                    },
                    function () {
                        self.name = name;
                        self.x = destX;
                        self.y = destY;
                        return self.animateIn($(self.name));
                    }
            ]);
        }
        return promiseUnit();
    },

};
