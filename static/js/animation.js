var animateIn = function($el) {
    var $elIn = $el.find('.in');
    var continuations = new Array();
    [1, 2, 3, 4, 5, 6, 7, 8, 9].forEach(function (i) {
        continuations.push(function () {
            var $elInOrd = $elIn.filter('.ord'+i);
            var deferred = new $.Deferred();
            var count = 1;
            var resolveOnCount = function () {
                --count;
                if (count == 0) {
                    deferred.resolve();
                }
            };
            $elInOrd.filter('.fade').animate(
                {opacity: '1.0'},
                'slow'
            ).promise().then(resolveOnCount);
            return deferred.promise();
        });
    });
    promisePipe(promiseUnit(), continuations);
}
