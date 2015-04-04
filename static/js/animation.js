var SlrAnimation = function () {
};

SlrAnimation.prototype = {

    classname: {
        'in': '.in',
        'out': '.out'
    },

    fade: {
        'in': {opacity: '1.0'},
        'out': {opacity: '0.0'}
    },

    animate: function ($rootEl, type) {
        var self = this;
        var $el = $rootEl.find(this.classname[type]);
        var continuations = new Array();
        [1, 2, 3, 4, 5, 6, 7, 8, 9].forEach(function (i) {
            continuations.push(function () {
                var $elInOrd = $el.filter('.ord'+i);
                var deferred = new $.Deferred();
                var count = 1;
                var resolveOnCount = function () {
                    --count;
                    if (count == 0) {
                        deferred.resolve();
                    }
                };
                $elInOrd.filter('.fade').animate(
                    self.fade[type],
                    'slow'
                ).promise().then(resolveOnCount);
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
