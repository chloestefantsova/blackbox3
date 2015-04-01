var fadeInAll = function ($el) {
    var promise = $el.find('.faded1').fadeIn('slow').promise();
    for (var i = 2; i < 10; ++i) {
        (function (index) {
            promise = promiseBind(promise, function () {
                console.log('working with .faded'+index);
                return $el.find('.faded'+index).fadeIn('slow').promise();
            });
        })(i);
    }
    promise.then(function () { console.log('done with animations'); });
}
