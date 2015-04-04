var SlrAnimation = function () {
};

SlrAnimation.prototype = {

    fade: {
        'in': function ($rootEl, order) {
            var selector = '.in'+order+'-fade';
            return $rootEl.find(selector).animate({opacity: '1.0'}, 'slow').promise();
        },
        'out': function ($rootEl, order) {
            var selector = '.out'+order+'-fade';
            return $rootEl.find(selector).animate({opacity: '0.0'}, 'slow').promise();
        }
    },

    animate: function ($rootEl, type) {
        var self = this;
        var continuations = new Array();
        [1, 2, 3, 4, 5, 6, 7, 8, 9].forEach(function (i) {
            continuations.push(function () {
                var deferred = new $.Deferred();
                var count = 1;
                var resolveOnCount = function () {
                    --count;
                    if (count == 0) {
                        deferred.resolve();
                    }
                };
                self.fade[type]($rootEl, i).then(resolveOnCount);
                return deferred.promise();
            });
        });
        promisePipe(promiseUnit(), continuations);
    },

    animateIn: function ($rootEl) {
        return this.animate($rootEl, 'in');
    },

    animateOut: function ($rootEl) {
        return this.animate($rootEl, 'out');
    },

};
